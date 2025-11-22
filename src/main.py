"""MCP server for GlobalPayments API integration."""

import os
from dotenv import load_dotenv
from mcp.server import FastMCP

# Load environment variables
load_dotenv()

# Import authentication and capabilities
from src.auth import TokenManager
from src.capabilities.links import LinksCapability
from src.models import PaymentRequest, PaymentLinkRequest, PaymentLinkListRequest

# Initialize server
server = FastMCP("mcp-gpapi")

# Initialize token manager (singleton)
auth_manager = TokenManager()

# Initialize capabilities
links = LinksCapability(auth_manager)

# Register tools

## Legacy tool (keep for backwards compatibility)
@server.tool()
async def process_payment(params: PaymentRequest):
    """Process a payment transaction (legacy mock)."""
    return {
        "status": "success",
        "transaction_id": "12345",
        "amount": params.amount,
        "currency": params.currency,
        "description": params.description
    }

## Payment Links
@server.tool()
async def send_payment_link(params: PaymentLinkRequest):
    """
    Create a payment link for a customer.
    
    Args:
        amount: Payment amount in dollars (e.g., 15.99)
        currency: Currency code (e.g., "USD") 
        description: Payment description
        reference: Optional unique reference
        name: Optional link name
        
    Returns:
        Payment link URL and details
    """
    return await links.create_payment_link(
        amount=params.amount,
        currency=params.currency,
        description=params.description,
        reference=params.reference,
        name=params.name
    )

@server.tool()
async def get_payment_link(link_id: str):
    """
    Retrieve payment link details.
    
    Args:
        link_id: Payment link ID
        
    Returns:
        Payment link details including status
    """
    return await links.get_payment_link(link_id)

@server.tool()
async def list_payment_links(params: PaymentLinkListRequest):
    """
    List payment links with optional filters.
    
    Args:
        from_time: Optional start timestamp (ISO 8601)
        to_time: Optional end timestamp (ISO 8601)
        page: Page number (default: 1)
        page_size: Results per page (default: 10)
        
    Returns:
        List of payment links
    """
    return await links.list_payment_links(
        from_time=params.from_time,
        to_time=params.to_time,
        page=params.page,
        page_size=params.page_size
    )

# Start server
if __name__ == "__main__":
    try:
        server.run()
    except Exception as e:
        print(f"Error starting server: {e}")