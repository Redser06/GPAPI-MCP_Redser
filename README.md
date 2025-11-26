# GlobalPayments MCP Server

A Model Context Protocol (MCP) server for integrating with the GlobalPayments API. This server provides a comprehensive set of tools for processing payments, managing transactions, tokenizing payment methods, and handling security/risk assessments.

## Features

### 1. Payment Links
- **Create Payment Link**: Generate secure links for customers to pay.
- **Manage Links**: List and retrieve payment link details.

### 2. Core Transactions
- **Sales**: Process direct sales (Authorize + Capture).
- **Refunds**: Refund full or partial amounts.
- **Captures**: Capture pre-authorized transactions.
- **Voids**: Reverse transactions before settlement.
- **Reporting**: List and query transaction history.

### 3. Security & Tokenization
- **Tokenization**: Store payment methods securely (create, update, delete, list tokens).
- **Authentication**: Initiate 3D Secure (3DS) authentication flows.
- **Risk Assessment**: Perform pre-transaction fraud checks.

## Configuration

### Environment Variables
Create a `.env` file in the root directory with the following credentials:

```env
# GlobalPayments Credentials
GP_APP_ID=your_app_id
GP_APP_KEY=your_app_key
GP_ENVIRONMENT=sandbox  # or production
GP_ACCOUNT_NAME=transaction_processing  # Your account name
GP_MERCHANT_ID=your_merchant_id
GP_ACCOUNT_ID=your_account_id

# Google API Key (if using Gemini)
GOOGLE_API_KEY=your_google_api_key
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MCP-gpapi
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

## Usage

### Running the Server
```bash
python -m src.main
```

### Available Tools

#### Payment Links
- `send_payment_link(amount, currency, description, ...)`
- `get_payment_link(link_id)`
- `list_payment_links(page, page_size, ...)`

#### Transactions
- `create_sale(amount, currency, payment_method, ...)`
- `refund_transaction(transaction_id, amount, ...)`
- `capture_transaction(transaction_id, amount, ...)`
- `void_transaction(transaction_id, ...)`
- `get_transaction(transaction_id)`
- `list_transactions(page, page_size, status, ...)`

#### Tokenization
- `create_token(payment_method, usage_mode, ...)`
- `get_token(token_id)`
- `update_token(token_id, ...)`
- `delete_token(token_id)`
- `list_tokens(customer_id, ...)`

#### Security
- `initiate_authentication(amount, currency, payment_method, ...)`
- `assess_risk(amount, currency, payment_method, ...)`

#### Disputes
- `list_disputes(page, page_size, status, ...)`
- `get_dispute(dispute_id)`
- `accept_dispute(dispute_id)`
- `challenge_dispute(dispute_id, evidence_text, ...)`

## Development

### Project Structure
```
src/
├── auth/           # Authentication logic (TokenManager)
├── capabilities/   # API capabilities (Links, Transactions, Tokens, etc.)
├── models/         # Pydantic data models
├── utils/          # Helper functions
└── main.py         # Server entry point
```

### Testing
Run the verification scripts to test connectivity:
```bash
python test_transactions.py
python test_tokens.py
```