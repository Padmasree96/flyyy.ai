# Optimized and Robust Extractor
import pandas as pd
from typing import List, Dict
from models.boq_schema import ExtractedItem
from utils.text_cleaner import clean_text, clean_quantity, is_valid_row
from config.settings import INVALID_ROW_KEYWORDS
from loguru import logger

def extract_boq(df: pd.DataFrame, column_map: Dict[str, str]) -> List[ExtractedItem]:
    """Extract data into standardized models with filtering and cleaning."""
    
    needed_cols = list(column_map.values())
    working_df = df[needed_cols].copy()
    
    results = []
    
    # Use itertuples for 5-10x better performance than iterrows
    for row in working_df.itertuples(index=False):
        try:
            row_dict = dict(zip(needed_cols, row))
            
            # Extract raw values
            raw_product = row_dict.get(column_map.get("product"))
            raw_brand = row_dict.get(column_map.get("brand"))
            raw_qty = row_dict.get(column_map.get("quantity"))
            raw_category = row_dict.get(column_map.get("category"))

            # 1. Skip invalid rows (TOTAL, SUBTOTAL, etc.)
            product_cleaned = clean_text(raw_product)
            if not is_valid_row(product_cleaned, INVALID_ROW_KEYWORDS):
                logger.debug(f"Skipping junk/total row: {product_cleaned}")
                continue

            # 2. Skip empty rows
            if not product_cleaned or product_cleaned.lower() in ["none", "nan", ""]:
                continue

            # 3. Clean and map data
            item_data = {
                "product": product_cleaned,
                "brand": clean_text(raw_brand) or "Generic",
                "quantity": clean_quantity(raw_qty),
                "category": clean_text(raw_category) or "Uncategorized"
            }

            # 4. Strict Schema Validation
            validated_item = ExtractedItem(**item_data)
            results.append(validated_item)

        except Exception as e:
            logger.error(f"Error processing row: {e}")
            continue
        
    return results