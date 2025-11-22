"""Base capability class for GlobalPayments API integrations."""

from typing import Dict, Any
import sys
import requests
from abc import ABC

from ..auth import TokenManager


class BaseCapability(ABC):
    """
    Base class for all GlobalPayments API capability modules.
    
    Provides common functionality:
    - Authentication via TokenManager
    - Standardized request handling
    - Error handling
    - Response formatting
    """
    
    def __init__(self, auth_manager: TokenManager):
        """
        Initialize capability with authentication manager.
        
        Args:
            auth_manager: TokenManager instance for API authentication
        """
        self.auth = auth_manager
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
        scope: str = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated request to GlobalPayments API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., '/ucp/transactions')
            data: Request body data
            params: Query parameters
            scope: Optional token scope
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.HTTPError: On HTTP errors
        """
        token = self.auth.get_token(scope=scope)
        url = f"{self.auth.base_url}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GP-Version": "2021-03-22"
        }
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print(f"API Error ({method} {endpoint}): {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                error_body = e.response.text
                print(f"Response: {error_body}", file=sys.stderr)
                return {"error": f"API Error: {error_body}"}
            return {"error": str(e)}
        
        except Exception as e:
            print(f"Unexpected error ({method} {endpoint}): {e}", file=sys.stderr)
            return {"error": str(e)}
    
    def _format_amount(self, amount: float) -> str:
        """
        Convert amount to cents format required by GP API.
        
        Args:
            amount: Amount in dollars (e.g., 15.99)
            
        Returns:
            Amount in cents as string (e.g., "1599")
        """
        return str(int(amount * 100))
