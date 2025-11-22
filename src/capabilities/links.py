"""Payment Links capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class LinksCapability(BaseCapability):
    """Payment links operations using GlobalPayments UCP API."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "transaction_processing")
    
    async def create_payment_link(
        self,
        amount: float,
        currency: str,
        description: str,
        reference: Optional[str] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a payment link.
        
        Args:
            amount: Amount in dollars (e.g., 15.99)
            currency: Currency code (e.g., "USD")
            description: Payment description
            reference: Optional unique reference
            name: Optional link name (defaults to truncated description)
            
        Returns:
            Payment link details including URL
        """
        amount_cents = self._format_amount(amount)
        
        payload = {
            "account_name": self.account_name,
            "type": "PAYMENT",
            "name": name or f"Payment Link - {description[:30]}",
            "usage_mode": "SINGLE",
            "description": description,
            "shippable": "NO",
            "reference": reference or f"REF-{os.urandom(4).hex()}",
            "transactions": {
                "amount": amount_cents,
                "currency": currency,
                "country": "US",
                "channel": "CNP",
                "allowed_payment_methods": ["CARD"]
            }
        }
       
        return self._make_request("POST", "/ucp/links", data=payload)
    
    async def get_payment_link(self, link_id: str) -> Dict[str, Any]:
        """
        Retrieve payment link details.
        
        Args:
            link_id: Payment link ID
            
        Returns:
            Payment link details
        """
        return self._make_request("GET", f"/ucp/links/{link_id}")
    
    async def list_payment_links(
        self,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        List payment links.
        
        Args:
            from_time: Start timestamp (ISO 8601)
            to_time: End timestamp (ISO 8601)
            page: Page number
            page_size: Results per page
            
        Returns:
            List of payment links
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if from_time:
            params["from_time_created"] = from_time
        if to_time:
            params["to_time_created"] = to_time
        
        return self._make_request("GET", "/ucp/links", params=params)
