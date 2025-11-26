"""Dispute capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class DisputeCapability(BaseCapability):
    """Dispute management operations."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "transaction_processing")
    
    async def list_disputes(
        self,
        page: int = 1,
        page_size: int = 10,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List disputes.
        
        Args:
            page: Page number
            page_size: Results per page
            from_time: Start time
            to_time: End time
            status: Filter by status
            
        Returns:
            List of disputes
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if from_time:
            params["from_time_created"] = from_time
        if to_time:
            params["to_time_created"] = to_time
        if status:
            params["status"] = status
            
        return self._make_request("GET", "/ucp/disputes", params=params)

    async def get_dispute(self, dispute_id: str) -> Dict[str, Any]:
        """
        Get dispute details.
        
        Args:
            dispute_id: Dispute ID
            
        Returns:
            Dispute details
        """
        return self._make_request("GET", f"/ucp/disputes/{dispute_id}")

    async def accept_dispute(self, dispute_id: str) -> Dict[str, Any]:
        """
        Accept a dispute (admit liability).
        
        Args:
            dispute_id: Dispute ID
            
        Returns:
            Result of acceptance
        """
        return self._make_request("POST", f"/ucp/disputes/{dispute_id}/accept")

    async def challenge_dispute(
        self,
        dispute_id: str,
        evidence_text: Optional[str] = None,
        documents: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Challenge a dispute with evidence.
        
        Args:
            dispute_id: Dispute ID
            evidence_text: Textual evidence
            documents: List of document IDs
            
        Returns:
            Result of challenge
        """
        payload = {}
        if evidence_text:
            payload["evidence_text"] = evidence_text
        if documents:
            payload["documents"] = documents
            
        return self._make_request("POST", f"/ucp/disputes/{dispute_id}/challenge", data=payload)
