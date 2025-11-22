import os
import sys
import time
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("GP_APP_ID")
APP_KEY = os.getenv("GP_APP_KEY")
ENVIRONMENT = os.getenv("GP_ENVIRONMENT", "sandbox")

def get_bearer_token():
    if not APP_ID or not APP_KEY:
        print("Error: GP_APP_ID or GP_APP_KEY not set")
        return None

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
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("token")
    except Exception as e:
        print(f"Error getting token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def list_merchants():
    token = get_bearer_token()
    if not token:
        return

    base_url = "https://apis.sandbox.globalpay.com" if ENVIRONMENT == "sandbox" else "https://apis.globalpay.com"
    url = f"{base_url}/ucp/merchants"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-GP-Version": "2021-03-22"
    }
    
    try:
        print(f"Listing merchants from {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("Merchants:", data)
        
        if data.get("merchants"):
            for merchant in data["merchants"]:
                merchant_id = merchant["id"]
                print(f"\nListing accounts for merchant {merchant_id} ({merchant['name']})...")
                accounts_url = f"{base_url}/ucp/merchants/{merchant_id}/accounts"
                try:
                    response = requests.get(accounts_url, headers=headers)
                    response.raise_for_status()
                    accounts_data = response.json()
                    print("Accounts:", accounts_data)
                    if accounts_data.get("accounts"):
                        print(f"FOUND ACCOUNT! Merchant: {merchant['name']}, Account: {accounts_data['accounts'][0]['name']}")
                        break
                except Exception as e:
                    print(f"Error listing accounts for {merchant_id}: {e}")
            
    except Exception as e:
        print(f"Error listing merchants/accounts: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    list_merchants()
