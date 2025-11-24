"""Transaction-related data models."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal


class TransactionDetail(BaseModel):
    """Details for a transaction."""
    amount: str  # Amount in cents
    currency: str
    country: Optional[str] = "US"
    channel: Optional[str] = "CNP"
    allowed_payment_methods: Optional[List[str]] = ["CARD"]


class SaleRequest(BaseModel):
    """Request model for creating a sale transaction."""
    amount: float = Field(..., description="Amount in dollars (e.g. 15.99)")
    currency: str = Field(..., description="Currency code (e.g. USD)")
    description: Optional[str] = None
    reference: Optional[str] = None
    payment_method: Optional[Dict[str, Any]] = Field(
        None, description="Payment method details (card, token, etc.)"
    )
    # For now we default these, but they could be parameterized
    country: str = "US"
    channel: str = "CNP"


class RefundRequest(BaseModel):
    """Request model for refunding a transaction."""
    amount: Optional[float] = Field(None, description="Amount to refund. If None, refunds full amount.")
    description: Optional[str] = None
    reference: Optional[str] = None


class CaptureRequest(BaseModel):
    """Request model for capturing a transaction."""
    amount: Optional[float] = Field(None, description="Amount to capture. If None, captures full amount.")
    description: Optional[str] = None
    reference: Optional[str] = None


class VoidRequest(BaseModel):
    """Request model for voiding a transaction."""
    description: Optional[str] = None
    reference: Optional[str] = None


class TransactionListRequest(BaseModel):
    """Request model for listing transactions."""
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    page: int = 1
    page_size: int = 10
    order_by: Optional[str] = "TIME_CREATED"
    order: Optional[str] = "DESC"
    status: Optional[str] = None
