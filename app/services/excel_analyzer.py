# ─── Multi-Sheet Excel Processing ───
import pandas as pd
from typing import List, Dict
from loguru import logger

from ..config.settings import HEADER_KEYWORDS, HEADER_SCAN_LIMIT, get_config
from .boq_table_detector import detect_header_row
from .boq_extractor import extract_items


def process_excel(file_stream, industry: str = "construction") -> Dict:
    """
    Full pipeline:
    1. Open workbook
    2. Loop through every sheet
    3. Detect header, map columns, extract & validate items
    4. Aggregate results across all sheets
    """
    config = get_config(industry)
    xls = pd.ExcelFile(file_stream)
    all_items: List[Dict] = []
    sheets_processed: List[str] = []

    for sheet_name in xls.sheet_names:
        logger.info(f"── Processing sheet: {sheet_name}")
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

        # Detect header
        header_row = detect_header_row(df)
        logger.info(f"   Header detected at row {header_row}")

        # Extract items from this sheet
        items = extract_items(
            df,
            header_row,
            field_mapping=config["field_mapping"],
            threshold=config["thresholds"]["fuzzy_match"],
        )

        if items:
            sheets_processed.append(sheet_name)
            all_items.extend(items)

    return {
        "total_sheets": len(xls.sheet_names),
        "sheets_with_data": sheets_processed,
        "items": all_items,
    }