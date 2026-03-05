# Generalized Column Identifier
import pandas as pd
from typing import Dict, List
from utils.fuzzy_matcher import get_best_match
from utils.text_cleaner import normalize_header
from loguru import logger

def identify_columns(df_columns: List[str], industry_mapping: Dict[str, List[str]], threshold: int = 70) -> Dict[str, str]:
    """Map Excel columns to standard internal field names using config and fuzzy matching."""
    
    mapping_result = {}
    available_cols = [str(c) for c in df_columns if c and not pd.isna(c)]
    logger.debug(f"Identifying columns from: {available_cols}")
    
    for internal_field, aliases in industry_mapping.items():
        found = False
        for alias in aliases:
            match = get_best_match(alias, available_cols, threshold=threshold)
            if match:
                mapping_result[internal_field] = match
                logger.info(f"Mapped internal field '{internal_field}' to Excel column '{match}' (via alias '{alias}')")
                found = True
                break
        if not found:
            logger.warning(f"Could not find a match for internal field: {internal_field}")
                
    return mapping_result