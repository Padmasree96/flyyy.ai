# ─── Column Identification (Fuzzy Matching) ───
import pandas as pd
from typing import Dict, List
from loguru import logger

from ..utils.fuzzy_matcher import get_best_match


def identify_columns(
    df_columns: List[str],
    field_mapping: Dict[str, List[str]],
    threshold: int = 70,
) -> Dict[str, str]:
    """Map Excel column headers to internal field names using fuzzy matching."""
    mapping_result: Dict[str, str] = {}
    available_cols = [str(c) for c in df_columns if c and not pd.isna(c)]
    logger.debug(f"Available columns: {available_cols}")

    for internal_field, aliases in field_mapping.items():
        for alias in aliases:
            match = get_best_match(alias, available_cols, threshold=threshold)
            if match:
                mapping_result[internal_field] = match
                logger.info(
                    f"Mapped '{internal_field}' → '{match}' (alias '{alias}')"
                )
                break
        else:
            logger.warning(f"No match for internal field: {internal_field}")

    return mapping_result