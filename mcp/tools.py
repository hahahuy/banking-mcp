"""MCP tool definitions for banking domain."""

from typing import TypedDict


class TransferRequest(TypedDict):
    amount: int
    from_account: str
    to_account: str
    recipient_bank: str


class BalanceResponse(TypedDict):
    account_id: str
    balance: int
    currency: str
    available_balance: int


class TransferResponse(TypedDict):
    transaction_id: str
    status: str
    amount: int
    fee: int
    timestamp: str


def get_account_balance(account_id: str) -> BalanceResponse:
    """Get account balance. Mock implementation."""
    return BalanceResponse(
        account_id=account_id,
        balance=50_000_000,
        currency="VND",
        available_balance=48_500_000,
    )


def transfer_money(request: TransferRequest) -> TransferResponse:
    """Transfer money between accounts. Mock implementation."""
    import uuid
    from datetime import datetime
    fee = 7_000 if request["amount"] < 100_000_000 else 0
    return TransferResponse(
        transaction_id=str(uuid.uuid4())[:8],
        status="completed",
        amount=request["amount"],
        fee=fee,
        timestamp=datetime.now().isoformat(),
    )


def get_transaction_history(account_id: str, limit: int = 10) -> dict:
    """Get recent transaction history. Mock implementation."""
    return {
        "account_id": account_id,
        "transactions": [
            {
                "id": f"txn_{i}",
                "amount": 500_000 * (i + 1),
                "type": "transfer_in" if i % 2 == 0 else "transfer_out",
                "timestamp": "2026-05-10T10:00:00Z",
            }
            for i in range(min(limit, 5))
        ],
    }


def lookup_policy(question: str) -> str:
    """Look up banking policy. Mock implementation."""
    policies = {
        "daily limit": "Daily transfer limit is 500,000,000 VND for standard accounts.",
        "interest rate": "Current annual interest rate is 4.5% for standard savings accounts.",
        "fraud": "You are protected by our zero-liability policy for verified unauthorized transactions.",
    }
    q = question.lower()
    for key, value in policies.items():
        if all(word in q for word in key.split()):
            return value
    return "Please contact our 24/7 hotline for more information."