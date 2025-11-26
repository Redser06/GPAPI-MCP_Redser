"""Settlement reporting data models."""

from pydantic import BaseModel
from typing import Optional


class SettlementListRequest(BaseModel):
    """Request model for listing settlements."""
    page: int = 1
    page_size: int = 10
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    status: Optional[str] = None
