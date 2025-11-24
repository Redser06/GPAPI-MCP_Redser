"""Tokenization capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class TokenCapability(BaseCapability):
    """Tokenization operations using GlobalPayments UCP API."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "tokenization")
    
    async def create_token(
        self,
        payment_method: Dict[str, Any],
        description: Optional[str] = None,
        customer_id: Optional[str] = None,
        usage_mode: str = "MULTIPLE"
    ) -> Dict[str, Any]:
        """
        Tokenize a payment method for future use.
        
        Args:
            payment_method: Card details or other method
            description: Token description
            customer_id: Customer identifier
            usage_mode: SINGLE or MULTIPLE
            
        Returns:
            Token details
        """
        payload = {
            "account_name": self.account_name,
            "type": "PAYMENT_METHOD",
            "usage_mode": usage_mode,
            "payment_method": payment_method
        }
        
        if description:
            payload["description"] = description
        if customer_id:
            payload["customer_id"] = customer_id
            
        return self._make_request("POST", "/ucp/payment-methods", data=payload)

    async def get_token(self, token_id: str) -> Dict[str, Any]:
        """
        Retrieve token details.
        
        Args:
            token_id: Token ID
            
        Returns:
            Token details
        """
        return self._make_request("GET", f"/ucp/payment-methods/{token_id}")

    async def delete_token(self, token_id: str) -> Dict[str, Any]:
        """
        Delete a stored token.
        
        Args:
            token_id: Token ID
            
        Returns:
            Deletion confirmation
        """
        return self._make_request("DELETE", f"/ucp/payment-methods/{token_id}")

    async def update_token(
        self,
        token_id: str,
        description: Optional[str] = None,
        customer_id: Optional[str] = None,
        expiry_month: Optional[str] = None,
        expiry_year: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update token details (e.g. expiry).
        
        Args:
            token_id: Token ID
            description: New description
            customer_id: New customer ID
            expiry_month: New expiry month
            expiry_year: New expiry year
            
        Returns:
            Updated token details
        """
        payload = {}
        
        if description:
            payload["description"] = description
        if customer_id:
            payload["customer_id"] = customer_id
            
        if expiry_month or expiry_year:
            payload["payment_method"] = {}
            if expiry_month:
                payload["payment_method"]["expiry_month"] = expiry_month
            if expiry_year:
                payload["payment_method"]["expiry_year"] = expiry_year
                
        return self._make_request("PATCH", f"/ucp/payment-methods/{token_id}", data=payload)

    async def list_tokens(
        self,
        page: int = 1,
        page_size: int = 10,
        customer_id: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List stored tokens.
        
        Args:
            page: Page number
            page_size: Results per page
            customer_id: Filter by customer
            from_time: Start time
            to_time: End time
            
        Returns:
            List of tokens
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if customer_id:
            params["customer_id"] = customer_id
        if from_time:
            params["from_time_created"] = from_time
        if to_time:
            params["to_time_created"] = to_time
            
        return self._make_request("GET", "/ucp/payment-methods", params=params)
