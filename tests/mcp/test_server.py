import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.mcp.tools import get_account_balance, transfer_money, lookup_policy


def test_get_account_balance():
    result = get_account_balance("ACC001")
    assert result["account_id"] == "ACC001"
    assert result["currency"] == "VND"
    assert result["balance"] > 0


def test_transfer_money():
    request = {
        "amount": 5_000_000,
        "from_account": "ACC001",
        "to_account": "ACC002",
        "recipient_bank": "TECHCOMBANK",
    }
    result = transfer_money(request)
    assert result["status"] == "completed"
    assert result["fee"] == 7000


def test_transfer_large_amount_no_fee():
    request = {
        "amount": 150_000_000,
        "from_account": "ACC001",
        "to_account": "ACC002",
        "recipient_bank": "VIETINBANK",
    }
    result = transfer_money(request)
    assert result["fee"] == 0


def test_lookup_policy_daily_limit():
    result = lookup_policy("What is my daily transfer limit?")
    assert "500,000,000" in result


def test_lookup_policy_unknown():
    result = lookup_policy("What is the weather?")
    assert "hotline" in result