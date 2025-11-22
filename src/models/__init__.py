"""Common data models for GlobalPayments API."""

from pydantic import BaseModel
from typing import Optional, Literal


class PaymentRequest(BaseModel):
    """Legacy payment request model (for backwards compatibility)."""
    amount: float
    currency: str
    description: str


class PaymentLinkRequest(BaseModel):
    """Request model for creating payment links."""
    amount: float
    currency: str
    description: str
    reference: Optional[str] = None
    name: Optional[str] = None


class PaymentLinkListRequest(BaseModel):
    """Request model for listing payment links."""
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    page: int = 1
    page_size: int = 10
