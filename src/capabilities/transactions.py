"""Transaction capability for GlobalPayments API."""

import os
from typing import Dict, Any, Optional
from .base import BaseCapability


class TransactionCapability(BaseCapability):
    """Transaction operations using GlobalPayments UCP API."""
    
    def __init__(self, auth_manager):
        super().__init__(auth_manager)
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "transaction_processing")
    
    async def create_sale(
        self,
        amount: float,
        currency: str,
        reference: Optional[str] = None,
        description: Optional[str] = None,
        payment_method: Optional[Dict[str, Any]] = None,
        country: str = "US",
        channel: str = "CNP"
    ) -> Dict[str, Any]:
        """
        Create a sale transaction (Authorize + Capture).
        
        Args:
            amount: Amount in dollars
            currency: Currency code
            reference: Unique reference
            description: Transaction description
            payment_method: Payment method details (card, token)
            country: Country code
            channel: Channel (CNP, CP)
            
        Returns:
            Transaction response
        """
        amount_cents = self._format_amount(amount)
        
        payload = {
            "account_name": self.account_name,
            "type": "SALE",
            "usage_mode": "SINGLE",
            "reference": reference or f"REF-{os.urandom(4).hex()}",
            "amount": amount_cents,
            "currency": currency,
            "country": country,
            "channel": channel
        }
        
        if description:
            payload["description"] = description
            
        if payment_method:
            payload["payment_method"] = payment_method
            
        return self._make_request("POST", "/ucp/transactions", data=payload)

    async def refund_transaction(
        self,
        transaction_id: str,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Refund a transaction.
        
        Args:
            transaction_id: ID of transaction to refund
            amount: Optional amount to refund (partial). If None, full refund.
            description: Refund description
            reference: Refund reference
            
        Returns:
            Refund response
        """
        payload = {
            "account_name": self.account_name,
            "type": "REFUND",
            "reference": reference or f"REFUND-{os.urandom(4).hex()}"
        }
        
        if amount is not None:
            payload["amount"] = self._format_amount(amount)
            
        if description:
            payload["description"] = description
            
        return self._make_request("POST", f"/ucp/transactions/{transaction_id}/refund", data=payload)

    async def capture_transaction(
        self,
        transaction_id: str,
        amount: Optional[float] = None,
        description: Optional[str] = None,
        reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Capture a previously authorized transaction.
        
        Args:
            transaction_id: ID of transaction to capture
            amount: Optional amount to capture. If None, full amount.
            description: Capture description
            reference: Capture reference
            
        Returns:
            Capture response
        """
        payload = {
            "account_name": self.account_name,
            "type": "CAPTURE",
            "reference": reference or f"CAP-{os.urandom(4).hex()}"
        }
        
        if amount is not None:
            payload["amount"] = self._format_amount(amount)
            
        if description:
            payload["description"] = description
            
        return self._make_request("POST", f"/ucp/transactions/{transaction_id}/capture", data=payload)

    async def void_transaction(
        self,
        transaction_id: str,
        description: Optional[str] = None,
        reference: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Void a transaction (cancel before settlement).
        
        Args:
            transaction_id: ID of transaction to void
            description: Void description
            reference: Void reference
            
        Returns:
            Void response
        """
        payload = {
            "account_name": self.account_name,
            "type": "REVERSAL",  # GP uses REVERSAL for void
            "reference": reference or f"VOID-{os.urandom(4).hex()}"
        }
        
        if description:
            payload["description"] = description
            
        return self._make_request("POST", f"/ucp/transactions/{transaction_id}/reversal", data=payload)

    async def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get details of a specific transaction.
        
        Args:
            transaction_id: Transaction ID
            
        Returns:
            Transaction details
        """
        return self._make_request("GET", f"/ucp/transactions/{transaction_id}")

    async def list_transactions(
        self,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        order_by: str = "TIME_CREATED",
        order: str = "DESC",
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List transactions with filtering.
        
        Args:
            from_time: Start time (ISO 8601)
            to_time: End time (ISO 8601)
            page: Page number
            page_size: Results per page
            order_by: Field to order by
            order: ASC or DESC
            status: Filter by status
            
        Returns:
            List of transactions
        """
        params = {
            "page": page,
            "page_size": page_size,
            "order_by": order_by,
            "order": order
        }
        
        if from_time:
            params["from_time_created"] = from_time
        if to_time:
            params["to_time_created"] = to_time
        if status:
            params["status"] = status
            
        return self._make_request("GET", "/ucp/transactions", params=params)
