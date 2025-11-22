"""Payment transaction tools for the MCP server."""

from pydantic import BaseModel
from typing import Dict, Any
import os
import sys
import requests
import hashlib
import time
import json

class PaymentRequest(BaseModel):
    amount: float
    currency: str
    description: str

class PaymentTools:
    """Payment-related tools."""

    def __init__(self):
        self.app_id = os.getenv("GP_APP_ID")
        self.app_key = os.getenv("GP_APP_KEY")
        self.account_name = os.getenv("GP_ACCOUNT_NAME", "ECOM")
        self.account_id = os.getenv("GP_ACCOUNT_ID")
        self.merchant_id = os.getenv("GP_MERCHANT_ID")
        self.environment = os.getenv("GP_ENVIRONMENT", "sandbox")
        
        if not self.app_id or not self.app_key:
            print("WARNING: GP_APP_ID or GP_APP_KEY not set in environment", file=sys.stderr)

    async def process_payment(self, params: PaymentRequest) -> Dict[str, Any]:
        """Process a payment transaction."""
        # In a real implementation, this would interact with a payment processor
        result = {
            "status": "success",
            "transaction_id": "12345",
            "amount": params.amount,
            "currency": params.currency,
            "description": params.description
        }
        
        return result

    def _get_bearer_token(self) -> str:
        """Exchange App ID and Key for a Bearer Token."""
        if not self.app_id or not self.app_key:
            raise ValueError("GP_APP_ID or GP_APP_KEY not set")

        nonce = str(int(time.time() * 1000))
        secret_raw = nonce + self.app_key
        secret = hashlib.sha512(secret_raw.encode()).hexdigest()
        
        base_url = "https://apis.sandbox.globalpay.com" if self.environment == "sandbox" else "https://apis.globalpay.com"
        url = f"{base_url}/ucp/accesstoken"
        
        headers = {
            "Content-Type": "application/json",
            "X-GP-Version": "2021-03-22"
        }
        
        payload = {
            "app_id": self.app_id,
            "nonce": nonce,
            "secret": secret,
            "grant_type": "client_credentials"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("token")

    async def send_payment_link(self, amount: float, currency: str, description: str, reference: str = None) -> Dict[str, Any]:
        """Generate a payment link using GlobalPayments API."""
        try:
            token = self._get_bearer_token()
        except Exception as e:
            return {"error": f"Authentication failed: {str(e)}"}
            
        base_url = "https://apis.sandbox.globalpay.com" if self.environment == "sandbox" else "https://apis.globalpay.com"
        url = f"{base_url}/ucp/links"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GP-Version": "2021-03-22"
        }
        
        # Convert amount to cents (integer)
        amount_in_cents = str(int(amount * 100))
        
        payload = {
            "account_name": "transaction_processing",
            "type": "PAYMENT",
            "name": f"Payment Link - {description[:30]}",
            "usage_mode": "SINGLE",
            "description": description,
            "shippable": "NO",
            "reference": reference or f"REF-{os.urandom(4).hex()}",
            "transactions": {
                "amount": amount_in_cents,
                "currency": currency,
                "country": "US",
                "channel": "CNP",
                "allowed_payment_methods": ["CARD"]
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating payment link: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                 return {"error": f"API Error: {e.response.text}"}
            return {"error": str(e)}