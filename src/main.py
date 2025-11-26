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
from src.capabilities.tokens import TokenCapability
from src.capabilities.authentication import AuthenticationCapability
from src.capabilities.risk import RiskCapability
from src.capabilities.disputes import DisputeCapability
from src.capabilities.settlements import SettlementCapability
from src.models import PaymentRequest, PaymentLinkRequest, PaymentLinkListRequest
from src.models.transaction import (
    SaleRequest, RefundRequest, CaptureRequest, VoidRequest, TransactionListRequest
)
from src.models.token import TokenRequest, TokenUpdateRequest, TokenListRequest
from src.models.dispute import DisputeListRequest, DisputeChallengeRequest
from src.models.settlement import SettlementListRequest

# Initialize server
server = FastMCP("mcp-gpapi")

# Initialize token manager (singleton)
auth_manager = TokenManager()

# Initialize capabilities
# Initialize capabilities
links = LinksCapability(auth_manager)
transactions = TransactionCapability(auth_manager)
tokens = TokenCapability(auth_manager)
authentication = AuthenticationCapability(auth_manager)
risk = RiskCapability(auth_manager)
disputes = DisputeCapability(auth_manager)
settlements = SettlementCapability(auth_manager)

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

## Tokenization Tools
@server.tool()
async def create_token(params: TokenRequest):
    """
    Create a payment token (store payment method).
    
    Args:
        params.payment_method: Card details
        params.description: Optional description
        params.customer_id: Optional customer ID
        params.usage_mode: "SINGLE" or "MULTIPLE"
        
    Returns:
        Token details
    """
    return await tokens.create_token(
        payment_method=params.payment_method,
        description=params.description,
        customer_id=params.customer_id,
        usage_mode=params.usage_mode
    )

@server.tool()
async def get_token(params: dict):
    """
    Get token details.
    
    Args:
        params.token_id: Token ID
        
    Returns:
        Token details
    """
    return await tokens.get_token(params["token_id"])

@server.tool()
async def delete_token(params: dict):
    """
    Delete a token.
    
    Args:
        params.token_id: Token ID
        
    Returns:
        Deletion confirmation
    """
    return await tokens.delete_token(params["token_id"])

@server.tool()
async def update_token(params: dict):
    """
    Update a token.
    
    Args:
        params.token_id: Token ID
        params.description: Optional description
        params.customer_id: Optional customer ID
        params.expiry_month: Optional expiry month
        params.expiry_year: Optional expiry year
        
    Returns:
        Updated token details
    """
    return await tokens.update_token(
        token_id=params["token_id"],
        description=params.get("description"),
        customer_id=params.get("customer_id"),
        expiry_month=params.get("expiry_month"),
        expiry_year=params.get("expiry_year")
    )

@server.tool()
async def list_tokens(params: TokenListRequest):
    """
    List stored tokens.
    
    Args:
        params.page: Page number
        params.page_size: Results per page
        params.customer_id: Filter by customer
        
    Returns:
        List of tokens
    """
    return await tokens.list_tokens(
        page=params.page,
        page_size=params.page_size,
        customer_id=params.customer_id,
        from_time=params.from_time,
        to_time=params.to_time
    )

## Authentication & Risk Tools
@server.tool()
async def initiate_authentication(params: dict):
    """
    Initiate 3DS authentication.
    
    Args:
        params.amount: Amount in dollars
        params.currency: Currency code
        params.payment_method: Card details
        params.reference: Optional reference
        
    Returns:
        Authentication response
    """
    return await authentication.initiate_authentication(
        amount=params["amount"],
        currency=params["currency"],
        payment_method=params["payment_method"],
        reference=params.get("reference"),
        country=params.get("country", "US")
    )

@server.tool()
async def assess_risk(params: dict):
    """
    Perform risk assessment.
    
    Args:
        params.amount: Amount in dollars
        params.currency: Currency code
        params.payment_method: Card details
        params.reference: Optional reference
        
    Returns:
        Risk assessment
    """
    return await risk.assess_risk(
        amount=params["amount"],
        currency=params["currency"],
        payment_method=params["payment_method"],
        reference=params.get("reference"),
        country=params.get("country", "US")
    )

## Operational Tools (Disputes & Settlements)
@server.tool()
async def list_disputes(params: DisputeListRequest):
    """
    List disputes.
    
    Args:
        params.page: Page number
        params.page_size: Results per page
        params.status: Filter by status
        
    Returns:
        List of disputes
    """
    return await disputes.list_disputes(
        page=params.page,
        page_size=params.page_size,
        from_time=params.from_time,
        to_time=params.to_time,
        status=params.status
    )

@server.tool()
async def get_dispute(params: dict):
    """
    Get dispute details.
    
    Args:
        params.dispute_id: Dispute ID
        
    Returns:
        Dispute details
    """
    return await disputes.get_dispute(params["dispute_id"])

@server.tool()
async def accept_dispute(params: dict):
    """
    Accept a dispute (admit liability).
    
    Args:
        params.dispute_id: Dispute ID
        
    Returns:
        Result of acceptance
    """
    return await disputes.accept_dispute(params["dispute_id"])

@server.tool()
async def challenge_dispute(params: dict):
    """
    Challenge a dispute.
    
    Args:
        params.dispute_id: Dispute ID
        params.evidence_text: Textual evidence
        params.documents: List of document IDs
        
    Returns:
        Result of challenge
    """
    return await disputes.challenge_dispute(
        dispute_id=params["dispute_id"],
        evidence_text=params.get("evidence_text"),
        documents=params.get("documents")
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