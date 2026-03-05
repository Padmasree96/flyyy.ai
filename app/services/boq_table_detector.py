# Configurable Table Detector
import pandas as pd
from typing import List, Optional
from utils.text_cleaner import normalize_header

def detect_boq_table(df: pd.DataFrame, keywords: List[str]) -> pd.DataFrame:
    """ Detect where the actual data table starts based on keywords. """
    
    # Iterate through rows to find header candidates
    for i in range(min(len(df), 20)):  
        row_values = df.iloc[i].dropna().astype(str).tolist()
        normalized_row = [v.lower() for v in row_values]
        
        # Check if any keyword matches a cell (even partially)
        found = False
        for k in keywords:
            k_low = k.lower()
            if any(k_low in cell for cell in normalized_row):
                found = True
                break
        
        if found:
            # Found the header!
            new_df = df.iloc[i+1:].copy()
            new_df.columns = df.iloc[i]
            return new_df.reset_index(drop=True)
            
    return df