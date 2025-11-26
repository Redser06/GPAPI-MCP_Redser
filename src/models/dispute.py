"""Dispute management data models."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class DisputeListRequest(BaseModel):
    """Request model for listing disputes."""
    page: int = 1
    page_size: int = 10
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    status: Optional[str] = None


class DisputeChallengeRequest(BaseModel):
    """Request model for challenging a dispute."""
    evidence_text: Optional[str] = Field(None, description="Textual evidence to support the challenge")
    documents: Optional[List[str]] = Field(None, description="List of document IDs to attach")
