# MCP GPAPI Server

This is a Model Context Protocol (MCP) server implementation for demonstrating payment transactions. It provides tools and capabilities for handling merchant transactions through a standardized protocol interface.

## Features

- MCP-compliant server implementation
- Support for payment transactions
- Tool-based interaction model
- Secure authorization handling
- Configurable via environment variables

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
GOOGLE_API_KEY=your_google_api_key
GP_ACCESS_TOKEN=your_global_payments_access_token
GP_ENVIRONMENT=sandbox  # or live
```

## Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install the package:
```bash
pip install -e .
```

3. Run the server:
```bash
python -m src.main
```

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

## License

Apache 2.0