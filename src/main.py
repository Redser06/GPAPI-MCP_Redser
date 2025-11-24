"""MCP server for GlobalPayments API integration."""

import os
from dotenv import load_dotenv
from mcp.server import FastMCP

# Load environment variables
load_dotenv()

# Import authentication and capabilities
from src.auth import TokenManager
from src.capabilities.links import LinksCapability
from src.capabilities.transactions import TransactionCapability
from src.models import PaymentRequest, PaymentLinkRequest, PaymentLinkListRequest
from src.models.transaction import (
    SaleRequest, RefundRequest, CaptureRequest, VoidRequest, TransactionListRequest
)

# Initialize server
server = FastMCP("mcp-gpapi")

# Initialize token manager (singleton)
auth_manager = TokenManager()

# Initialize capabilities
links = LinksCapability(auth_manager)
transactions = TransactionCapability(auth_manager)

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

## Transaction Tools
@server.tool()
async def create_sale(params: SaleRequest):
    """
    Create a sale transaction (Authorize + Capture).
    
    Args:
        params.amount: Amount in dollars
        params.currency: Currency code (e.g. USD)
        params.reference: Optional unique reference
        params.description: Optional description
        params.payment_method: Optional payment method details
        
    Returns:
        Transaction details
    """
    return await transactions.create_sale(
        amount=params.amount,
        currency=params.currency,
        reference=params.reference,
        description=params.description,
        payment_method=params.payment_method,
        country=params.country,
        channel=params.channel
    )

@server.tool()
async def refund_transaction(params: dict):
    """
    Refund a transaction.
    
    Args:
        params.transaction_id: ID of transaction to refund
        params.amount: Optional amount to refund (partial)
        params.description: Optional description
        params.reference: Optional reference
        
    Returns:
        Refund details
    """
    # Manually parse params since we need transaction_id from top level but others from model
    # For simplicity in this tool wrapper, we'll just extract from dict
    return await transactions.refund_transaction(
        transaction_id=params["transaction_id"],
        amount=params.get("amount"),
        description=params.get("description"),
        reference=params.get("reference")
    )

@server.tool()
async def capture_transaction(params: dict):
    """
    Capture a transaction.
    
    Args:
        params.transaction_id: ID of transaction to capture
        params.amount: Optional amount to capture
        params.description: Optional description
        params.reference: Optional reference
        
    Returns:
        Capture details
    """
    return await transactions.capture_transaction(
        transaction_id=params["transaction_id"],
        amount=params.get("amount"),
        description=params.get("description"),
        reference=params.get("reference")
    )

@server.tool()
async def void_transaction(params: dict):
    """
    Void (reverse) a transaction.
    
    Args:
        params.transaction_id: ID of transaction to void
        params.description: Optional description
        params.reference: Optional reference
        
    Returns:
        Void details
    """
    return await transactions.void_transaction(
        transaction_id=params["transaction_id"],
        description=params.get("description"),
        reference=params.get("reference")
    )

@server.tool()
async def get_transaction(params: dict):
    """
    Get transaction details.
    
    Args:
        params.transaction_id: Transaction ID
        
    Returns:
        Transaction details
    """
    return await transactions.get_transaction(params["transaction_id"])

@server.tool()
async def list_transactions(params: TransactionListRequest):
    """
    List transactions.
    
    Args:
        params.from_time: Start time (ISO 8601)
        params.to_time: End time (ISO 8601)
        params.page: Page number
        params.page_size: Results per page
        params.status: Filter by status
        
    Returns:
        List of transactions
    """
    return await transactions.list_transactions(
        from_time=params.from_time,
        to_time=params.to_time,
        page=params.page,
        page_size=params.page_size,
        order_by=params.order_by,
        order=params.order,
        status=params.status
    )

## Payment Links
@server.tool()
async def send_payment_link(params: PaymentLinkRequest):
    """
    Create a payment link for a customer.
    
    Args:
        params.amount: Payment amount in dollars (e.g., 15.99)
        params.currency: Currency code (e.g., "USD") 
        params.description: Payment description
        params.reference: Optional unique reference
        params.name: Optional link name
        
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
async def get_payment_link(params: dict):
    """
    Retrieve payment link details.
    
    Args:
        params.link_id: Payment link ID
        
    Returns:
        Payment link details including status
    """
    return await links.get_payment_link(params["link_id"])

@server.tool()
async def list_payment_links(params: PaymentLinkListRequest):
    """
    List payment links with optional filters.
    
    Args:
        params.from_time: Optional start timestamp (ISO 8601)
        params.to_time: Optional end timestamp (ISO 8601)
        params.page: Page number (default: 1)
        params.page_size: Results per page (default: 10)
        
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