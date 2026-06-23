import os

# Define the repository file matrix contents
files = {
"requirements.txt": """playwright==1.49.0
beautifulsoup4==4.12.3
pandas==2.2.3
gspread==6.1.2
pydantic==2.10.4
loguru==0.7.2
""",

"models.py": """from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

class ProductPayload(BaseModel):
    sku: str = Field(..., min_length=1, description="Unique Stock Keeping Unit identification hash.")
    title: str = Field(..., min_length=1, description="Sanitized structural canonical title of the product.")
    price: float = Field(..., gt=0.0, description="Normalized floating-point fiat currency cost.")
    currency: str = Field(default="USD", max_length=3)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("price", mode="before")
    @classmethod
    def sanitize_and_parse_price(cls, value: any) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            sanitized = re.sub(r"[^\\d.]", "", value)
            if sanitized:
                return float(sanitized)
        raise ValueError(f"Incompatible semantic type mapping for price value: {value}")
""",

"scraper.py": """import json
import asyncio
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Response
from loguru import logger
from models import ProductPayload

class ScrapingPipelineException(Exception):
    pass

class OperationalIngestionEngine:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.intercepted_json_payload: Optional[Dict[str, Any]] = None

    async def _network_traffic_sniffer(self, response: Response) -> None:
        try:
            if any(kapt in response.url.lower() for kapt in ["/api/v", "/graphql", "/product/detail"]):
                if response.status == 200:
                    raw_text = await response.text()
                    self.intercepted_json_payload = json.loads(raw_text)
                    logger.success(f"Network interceptor successfully drained API wire: {response.url[:60]}...")
        except Exception as ex:
            logger.debug(f"Transient non-blocking parsing exception caught during traffic sniffing: {ex}")

    async def execute_ingestion_cycle(self) -> ProductPayload:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = await context.new_page()
            page.on("response", self._network_traffic_sniffer)
            
            logger.info(f"Initiating extraction runtime targeting: {self.target_url}")
            try:
                await page.goto(self.target_url, wait_until="networkidle", timeout=45000)
            except Exception as context_timeout:
                logger.warning(f"Network timeout hit before networkidle achieved: {context_timeout}")

            if self.intercepted_json_payload:
                try:
                    logger.info("Evaluating Tier 1 payload: Native API data structural map processing.")
                    return ProductPayload(
                        sku=self.intercepted_json_payload.get("id") or self.intercepted_json_payload.get("sku"),
                        title=self.intercepted_json_payload.get("name") or self.intercepted_json_payload.get("title"),
                        price=self.intercepted_json_payload.get("price", {}).get("current") or self.intercepted_json_payload.get("amount")
                    )
                except Exception as tier_one_err:
                    logger.warning(f"Tier 1 collapsed. Escalating to Tier 2: {tier_one_err}")

            logger.info("Invoking Tier 2 Fallback Architecture: Compiling structural SEO schemas.")
            schema_node = await page.query_selector('script[type="application/ld+json"]')
            if schema_node:
                try:
                    raw_schema_text = await schema_node.inner_text()
                    schema_dict = json.loads(raw_schema_text)
                    if isinstance(schema_dict, list):
                        schema_dict = schema_dict[0]
                    return ProductPayload(
                        sku=schema_dict.get("sku") or schema_dict.get("mpn") or "UNKNOWN_SKU",
                        title=schema_dict.get("name", "Unknown Product Title"),
                        price=schema_dict.get("offers", {}).get("price") or schema_dict.get("offers", [{}])[0].get("price")
                    )
                except Exception as tier_two_err:
                    logger.warning(f"Tier 2 collapsed. Escalating to Tier 3 DOM parsing: {tier_two_err}")

            logger.info("Invoking Tier 3 Fallback Architecture: Resolving raw visual DOM state.")
            html_content = await page.content()
            await browser.close()
            
            from bs4 import BeautifulSoup
            import re
            soup = BeautifulSoup(html_content, "html.parser")
            try:
                title_node = soup.find("meta", property="og:title") or soup.find("h1")
                price_node = soup.find("meta", property="product:price:amount") or soup.find(class_=re.compile(r"(price|amount|cost)"))
                extracted_title = title_node["content"] if title_node.has_attr("content") else title_node.get_text()
                extracted_price = price_node["content"] if price_node.has_attr("content") else price_node.get_text()
                return ProductPayload(
                    sku=f"DOM_GENERATED_{hash(self.target_url)}",
                    title=extracted_title.strip(),
                    price=extracted_price
                )
            except Exception as final_tier_collapse:
                logger.critical("All processing tiers have systematically failed.")
                raise ScrapingPipelineException("Target dataset format is unparsable.") from final_tier_collapse
""",

"pipeline.py": """import os
from typing import List
import pandas as pd
import gspread
from loguru import logger
from models import ProductPayload

class GoogleSheetsSyncAdapter:
    def __init__(self, spreadsheet_id: str, credentials_path: str = "credentials.json"):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self._client: gspread.Client = self._authenticate_pool()

    def _authenticate_pool(self) -> gspread.Client:
        if not os.path.exists(self.credentials_path):
            logger.critical(f"Security runtime halted: Missing deployment credentials matrix at {self.credentials_path}")
            raise FileNotFoundError("Google Cloud Platform service account file missing.")
        return gspread.service_account(filename=self.credentials_path)

    def write_payload_matrix(self, payloads: List[ProductPayload], sheet_name: str = "Competitor Tracking") -> None:
        try:
            logger.info(f"Serializing {len(payloads)} structural payloads for spreadsheet extraction.")
            raw_records = [payload.model_dump() for payload in payloads]
            df = pd.DataFrame(raw_records)
            if "timestamp" in df.columns:
                df["timestamp"] = df["timestamp"].astype(str)

            spreadsheet = self._client.open_by_key(self.spreadsheet_id)
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="10")
                logger.info(f"Created new dynamic ledger worksheet: {sheet_name}")

            worksheet.clear()
            headers = [df.columns.values.tolist()]
            data_rows = df.values.tolist()
            total_matrix_payload = headers + data_rows
            worksheet.update(range_name="A1", values=total_matrix_payload)
            logger.success(f"Successfully synchronized {len(data_rows)} rows to Google Sheets ledger.")
        except Exception as api_err:
            logger.critical(f"Data ingestion link crashed during API transaction: {api_err}")
            raise api_err
""",

"main.py": """import asyncio
import sys
from loguru import logger
from scraper import OperationalIngestionEngine
from pipeline import GoogleSheetsSyncAdapter

logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>", level="INFO")

TARGET_MONITOR_URLS = [
    "
