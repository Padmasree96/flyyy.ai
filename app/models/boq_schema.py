# Generalized Items Schema
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ExtractedItem(BaseModel):
    product: str
    brand: Optional[str] = "Generic"
    quantity: float = 0
    category: Optional[str] = "Uncategorized"
    # Allow for any additional industry-specific fields
    extra_data: Dict[str, Any] = Field(default_factory=dict)