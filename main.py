import asyncio
import sys
from loguru import logger
from scraper import OperationalIngestionEngine
from pipeline import GoogleSheetsSyncAdapter

# Configure centralized production logging streams
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>", level="INFO")
logger.add("logs/production_pipeline.log", rotation="10 MB", retention="30 days", compression="zip", level="WARNING")

# Mock Targets Target Matrix - In a production setup, load these out of a database config table
TARGET_MONITOR_URLS = [
    "https://httpbin.org", # Target Stub Alpha
]

# Provide your real Google Sheet Unique Identifier ID hash here
GOOGLE_SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HASH_GOES_HERE"

async def main():
    logger.info("Initializing Enterprise Data Ingestion Pipeline Execution Matrix...")
    
    collected_payloads = []
    
    for idx, url in enumerate(TARGET_MONITOR_URLS, start=1):
        logger.info(f"Processing target task [{idx}/{len(TARGET_MONITOR_URLS)}] ──► {url}")
        
        engine = OperationalIngestionEngine(target_url=url)
        try:
            # Execute the multi-tier self-healing parser
            validated_product_record = await engine.execute_ingestion_cycle()
            collected_payloads.append(validated_product_record)
            
            # Defensive polite parsing delay between targets to mimic normal browser habits
            await asyncio.sleep(2.5)
            
        except Exception as error:
            logger.error(f"Pipeline bypassed broken record layout at URL ({url}). Execution continuing safely. Detail: {error}")
            continue

    if collected_payloads:
        try:
            # Initialize streaming sync link to cloud sheets engine
            adapter = GoogleSheetsSyncAdapter(spreadsheet_id=GOOGLE_SPREADSHEET_ID)
            adapter.write_payload_matrix(payloads=collected_payloads)
        except Exception as sync_fault:
            logger.critical(f"Master synchronization sequence failed: {sync_fault}")
    else:
        logger.warning("Data sync cancelled: Ingestion cycle yielded zero validated data models.")

if __name__ == "__main__":
    asyncio.run(main())
