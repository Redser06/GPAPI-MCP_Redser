import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from src.capabilities.transactions import TransactionCapability
from src.capabilities.tokens import TokenCapability
from src.capabilities.disputes import DisputeCapability
from src.capabilities.settlements import SettlementCapability
from src.auth.token_manager import TokenManager

class TestTransactionCapability(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_auth = MagicMock(spec=TokenManager)
        self.mock_auth.get_token = MagicMock(return_value="mock_token")
        self.transactions = TransactionCapability(self.mock_auth)
        # Mock the _make_request method as synchronous (MagicMock)
        self.transactions._make_request = MagicMock(return_value={"status": "success"})

    async def test_create_sale_payload(self):
        await self.transactions.create_sale(
            amount=10.00,
            currency="USD",
            reference="REF123",
            description="Test Sale"
        )
        
        # Verify arguments passed to _make_request
        self.transactions._make_request.assert_called_once()
        args, kwargs = self.transactions._make_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/ucp/transactions")
        
        payload = kwargs["data"]
        self.assertEqual(payload["amount"], "1000")  # Should be converted to cents
        self.assertEqual(payload["currency"], "USD")
        self.assertEqual(payload["reference"], "REF123")
        self.assertEqual(payload["type"], "SALE")

    async def test_refund_transaction(self):
        await self.transactions.refund_transaction("TRANS_ID", amount=5.50)
        
        self.transactions._make_request.assert_called_once()
        args, kwargs = self.transactions._make_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/ucp/transactions/TRANS_ID/refund")
        self.assertEqual(kwargs["data"]["amount"], "550")

class TestTokenCapability(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_auth = MagicMock(spec=TokenManager)
        self.tokens = TokenCapability(self.mock_auth)
        self.tokens._make_request = MagicMock(return_value={"status": "success"})

    async def test_create_token_payload(self):
        payment_method = {"card_number": "4111"}
        await self.tokens.create_token(
            payment_method=payment_method,
            customer_id="CUST_001"
        )
        
        self.tokens._make_request.assert_called_once()
        _, kwargs = self.tokens._make_request.call_args
        payload = kwargs["data"]
        self.assertEqual(payload["type"], "PAYMENT_METHOD")
        self.assertEqual(payload["usage_mode"], "MULTIPLE")
        self.assertEqual(payload["customer_id"], "CUST_001")

class TestDisputeCapability(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_auth = MagicMock(spec=TokenManager)
        self.disputes = DisputeCapability(self.mock_auth)
        self.disputes._make_request = MagicMock(return_value={"status": "success"})

    async def test_challenge_dispute_payload(self):
        await self.disputes.challenge_dispute(
            dispute_id="DSP_123",
            evidence_text="This charge is valid.",
            documents=["DOC_1", "DOC_2"]
        )
        
        self.disputes._make_request.assert_called_once()
        args, kwargs = self.disputes._make_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/ucp/disputes/DSP_123/challenge")
        
        payload = kwargs["data"]
        self.assertEqual(payload["evidence_text"], "This charge is valid.")
        self.assertEqual(payload["documents"], ["DOC_1", "DOC_2"])

class TestSettlementCapability(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_auth = MagicMock(spec=TokenManager)
        self.settlements = SettlementCapability(self.mock_auth)
        self.settlements._make_request = MagicMock(return_value={"status": "success"})

    async def test_list_settlements_params(self):
        await self.settlements.list_settlements(
            page=2,
            from_time="2023-01-01T00:00:00Z"
        )
        
        self.settlements._make_request.assert_called_once()
        _, kwargs = self.settlements._make_request.call_args
        params = kwargs["params"]
        self.assertEqual(params["page"], 2)
        self.assertEqual(params["from_time_created"], "2023-01-01T00:00:00Z")
        # self.assertEqual(params["order_by"], "TIME_CREATED")  # Removed default sort

if __name__ == "__main__":
    unittest.main()
