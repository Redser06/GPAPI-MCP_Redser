import os
import sys
import time
import hashlib
import requests
import json
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("GP_APP_ID")
APP_KEY = os.getenv("GP_APP_KEY")
ENVIRONMENT = os.getenv("GP_ENVIRONMENT", "sandbox")
ACCOUNT_NAME = os.getenv("GP_ACCOUNT_NAME", "my_merchants")
MERCHANT_ID = os.getenv("GP_MERCHANT_ID")
ACCOUNT_ID = os.getenv("GP_ACCOUNT_ID")

def get_bearer_token():
    nonce = str(int(time.time() * 1000))
    secret_raw = nonce + APP_KEY
    secret = hashlib.sha512(secret_raw.encode()).hexdigest()
    
    base_url = "https://apis.sandbox.globalpay.com" if ENVIRONMENT == "sandbox" else "https://apis.globalpay.com"
    url = f"{base_url}/ucp/accesstoken"
    
    headers = {
        "Content-Type": "application/json",
        "X-GP-Version": "2021-03-22"
    }
    
    payload = {
        "app_id": APP_ID,
        "nonce": nonce,
        "secret": secret,
        "grant_type": "client_credentials"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("token")

def test_create_link():
    token = get_bearer_token()
    print(f"Token: {token[:10]}...")
    
    base_url = "https://apis.sandbox.globalpay.com" if ENVIRONMENT == "sandbox" else "https://apis.globalpay.com"
    url = f"{base_url}/ucp/links"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-GP-Version": "2021-03-22"
    }
    
    # Test Payload 1: Transactions as Dict, with Merchant ID
    payload = {
        "account_name": "transaction_processing",
        "type": "PAYMENT",
        "name": "Pizza Payment Link",
        "usage_mode": "SINGLE",
        "description": "Test Pizza",
        "shippable": "NO",
        "reference": f"REF-{os.urandom(4).hex()}",
        "transactions": {
            "amount": "1599",
            "currency": "USD",
            "country": "US",
            "channel": "CNP",
            "allowed_payment_methods": ["CARD"]
        }
    }
    
    print("\nSending Payload:", json.dumps(payload, indent=2))
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print("Response:", response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_create_link()
