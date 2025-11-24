"""Risk assessment capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class RiskCapability(BaseCapability):
    """Risk assessment operations."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "transaction_processing")
    
    async def assess_risk(
        self,
        amount: float,
        currency: str,
        payment_method: Dict[str, Any],
        reference: Optional[str] = None,
        country: str = "US"
    ) -> Dict[str, Any]:
        """
        Perform risk assessment on a transaction.
        
        Args:
            amount: Amount in dollars
            currency: Currency code
            payment_method: Payment details
            reference: Unique reference
            country: Country code
            
        Returns:
            Risk score and decision
        """
        amount_cents = self._format_amount(amount)
        
        payload = {
            "account_name": self.account_name,
            "type": "RISK_ASSESSMENT",
            "usage_mode": "SINGLE",
            "reference": reference or f"RISK-{os.urandom(4).hex()}",
            "amount": amount_cents,
            "currency": currency,
            "country": country,
            "payment_method": payment_method
        }
        
        return self._make_request("POST", "/ucp/risk-assessments", data=payload)
