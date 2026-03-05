# Fuzzy Matching Utilities
from rapidfuzz import fuzz, process
from typing import List, Optional, Tuple

def get_best_match(target: str, candidates: List[str], threshold: int = 70) -> Optional[str]:
    """Find the best match for a string among a list of candidates."""
    if not target or not candidates:
        return None
    
    # Using WRatio (Weighted Ratio) which is highly robust for disparate lengths and partial matches
    match = process.extractOne(target.lower(), [c.lower() for c in candidates], scorer=fuzz.WRatio)
    
    if match and match[1] >= threshold:
        idx = [c.lower() for c in candidates].index(match[0])
        return candidates[idx]
    
    return None

def match_any(target: str, keywords: List[str], threshold: int = 85) -> bool:
    """Check if target matches any keyword."""
    for kw in keywords:
        if fuzz.partial_ratio(target.lower(), kw.lower()) >= threshold:
            return True
    return False
