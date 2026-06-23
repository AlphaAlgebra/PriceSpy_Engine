from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re

class ProductPayload(BaseModel):
    sku: str = Field(..., min_length=1, description="Unique Stock Keeping Unit identification hash.")
    title: str = Field(..., min_length=1, description="Sanitized, structural canonical title of the product.")
    price: float = Field(..., gt=0.0, description="Normalized floating-point fiat currency cost.")
    currency: str = Field(default="USD", max_length=3)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("price", mode="before")
    @classmethod
    def sanitize_and_parse_price(cls, value: any) -> float:
        """Defensive type-coercion engine to strip currency artifacts and parse floats cleanly."""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            sanitized = re.sub(r"[^\d.]", "", value)
            if sanitized:
                return float(sanitized)
        raise ValueError(f"Incompatible semantic type mapping for price value: {value}")
