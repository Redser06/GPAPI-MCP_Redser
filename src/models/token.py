"""Tokenization data models."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class TokenRequest(BaseModel):
    """Request model for creating a payment token."""
    payment_method: Dict[str, Any] = Field(..., description="Payment method details (card number, expiry, etc.)")
    description: Optional[str] = None
    customer_id: Optional[str] = None
    usage_mode: str = "MULTIPLE"  # Default to multiple use for tokens


class TokenUpdateRequest(BaseModel):
    """Request model for updating a payment token."""
    description: Optional[str] = None
    customer_id: Optional[str] = None
    expiry_month: Optional[str] = None
    expiry_year: Optional[str] = None


class TokenListRequest(BaseModel):
    """Request model for listing tokens."""
    page: int = 1
    page_size: int = 10
    customer_id: Optional[str] = None
    from_time: Optional[str] = None
    to_time: Optional[str] = None
