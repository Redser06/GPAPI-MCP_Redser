"""Authentication capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class AuthenticationCapability(BaseCapability):
    """3D Secure authentication operations."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "transaction_processing")
    
    async def initiate_authentication(
        self,
        amount: float,
        currency: str,
        payment_method: Dict[str, Any],
        reference: Optional[str] = None,
        country: str = "US"
    ) -> Dict[str, Any]:
        """
        Initiate 3DS authentication.
        
        Args:
            amount: Amount in dollars
            currency: Currency code
            payment_method: Card details
            reference: Unique reference
            country: Country code
            
        Returns:
            Authentication response (challenge or success)
        """
        amount_cents = self._format_amount(amount)
        
        payload = {
            "account_name": self.account_name,
            "type": "AUTHENTICATION",
            "usage_mode": "SINGLE",
            "reference": reference or f"AUTH-{os.urandom(4).hex()}",
            "amount": amount_cents,
            "currency": currency,
            "country": country,
            "payment_method": payment_method
        }
        
        return self._make_request("POST", "/ucp/authentications", data=payload)

    async def get_authentication(self, authentication_id: str) -> Dict[str, Any]:
        """
        Get authentication details.
        
        Args:
            authentication_id: Auth ID
            
        Returns:
            Auth details
        """
        return self._make_request("GET", f"/ucp/authentications/{authentication_id}")
