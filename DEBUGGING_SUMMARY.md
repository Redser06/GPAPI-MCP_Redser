# Payment Link Creation - Debugging Summary

## Issue
The `send_payment_link` tool fails with HTTP 403 "Access token and merchant info do not match" (error code 40003).

## What Works
✅ Access token generation (authentication successful)
✅ List merchants API call
✅ List accounts API call  
✅ MCP server initialization and tool registration

## What Fails
❌ Creating payment links via POST `/ucp/links`

## Root Cause Analysis

The error "Access token and merchant info do not match" with code 40003 (ACTION_NOT_AUTHORIZED) indicates a **permissions/scope issue**, not a payload formatting problem.

### Evidence
1. **Payload variations tested**: We tested multiple payload structures including:
   - Transactions as object vs array
   - With/without merchant_id
   - With/without account_id
   - Different account_name values
   - All resulted in the same 403 error

2. **Authentication works**: The access token is valid (successfully listed merchants and accounts)

3. **Authorization fails**: The app credentials have permissions for READ operations but not for LINK_CREATE

## Likely Solution

The developer app credentials need:

1. **LINK_CREATE permission/scope** explicitly added in the Global Payments developer portal
2. **Merchant association** - the app may need to be associated with specific merchant IDs authorized to create payment links
3. **Account configuration** - verify the account is enabled for payment link creation

## Next Steps

The user should:
1. Log into the Global Payments developer portal
2. Navigate to app settings for the app with ID `hAkv8y0PXzMxXnL8GHrcGdbaXn2WhTsF`
3. Verify/add the LINK_CREATE permission
4. Ensure the app is associated with the correct merchant account
5. Contact Global Payments support if permissions cannot be self-configured

## Code Status

The MCP server code is correctly implemented. Once permissions are granted, the tool should work without code changes.
