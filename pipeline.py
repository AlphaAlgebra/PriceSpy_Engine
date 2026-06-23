import os
from typing import List
import pandas as pd
import gspread
from loguru import logger
from models import ProductPayload
from scraper import OperationalIngestionEngine

class GoogleSheetsSyncAdapter:
    def __init__(self, spreadsheet_id: str, credentials_path: str = "credentials.json"):
        """
        Establishes an authorized connection pool to the Google Sheets API 
        using a secure service account credential matrix.
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self._client: gspread.Client = self._authenticate_pool()

    def _authenticate_pool(self) -> gspread.Client:
        if not os.path.exists(self.credentials_path):
            logger.critical(f"Security runtime halted: Missing deployment authorization matrix at {self.credentials_path}")
            raise FileNotFoundError("Google Cloud Platform service account file missing.")
        return gspread.service_account(filename=self.credentials_path)

    def write_payload_matrix(self, payloads: List[ProductPayload], sheet_name: str = "Competitor Tracking") -> None:
        """
        Serializes the validated Pydantic data matrices using Pandas 
        and flushes the dataset upstream to the live dashboard sheet in a single atomic batch write.
        """
        try:
            logger.info(f"Serializing {len(payloads)} structural payloads for spreadsheet extraction.")
            
            # Map structural data objects to records layout matrix
            raw_records = [payload.model_dump() for payload in payloads]
            df = pd.DataFrame(raw_records)
            
            # Format Datetime values to clean ISO string structures for non-technical users
            if "timestamp" in df.columns:
                df["timestamp"] = df["timestamp"].astype(str)

            # Open target worksheet ledger
            spreadsheet = self._client.open_by_key(self.spreadsheet_id)
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="10")
                logger.info(f"Created new dynamic ledger worksheet: {sheet_name}")

            # Prepare transactional state layout
            worksheet.clear()
            headers = [df.columns.values.tolist()]
            data_rows = df.values.tolist()
            total_matrix_payload = headers + data_rows

            # Atomic network call execution
            worksheet.update(range_name="A1", values=total_matrix_payload)
            logger.success(f"Successfully synchronized {len(data_rows)} rows to Google Sheets ledger.")
            
        except Exception as api_err:
            logger.critical(f"Data ingestion link crashed during Google Sheets API transaction: {api_err}")
            raise api_err
