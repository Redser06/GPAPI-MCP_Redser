"""Settlement capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class SettlementCapability(BaseCapability):
    """Settlement reporting operations."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "transaction_processing")
    
    async def list_settlements(
        self,
        page: int = 1,
        page_size: int = 10,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List settlement batches.
        
        Args:
            page: Page number
            page_size: Results per page
            from_time: Start time
            to_time: End time
            status: Filter by status
            
        Returns:
            List of settlements
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
            
        return self._make_request("GET", "/ucp/settlement-reports", params=params)

    async def get_settlement(self, settlement_id: str) -> Dict[str, Any]:
        """
        Get settlement batch details.
        
        Args:
            settlement_id: Settlement ID
            
        Returns:
            Settlement details
        """
        return self._make_request("GET", f"/ucp/settlements/{settlement_id}")
