# banking-mcp

Standalone MCP server exposing banking domain tools as a Model Context Protocol server.

## Overview

MCP server that provides four banking operations — balance inquiry, transfer, transaction history, and policy lookup — as tool endpoints compatible with the MCP specification. Designed to be consumed by the `banking-agent` orchestration layer, but is fully standalone.

## Architecture

```
Client (banking-agent)
    │
    └─ MCP protocol over stdio / HTTP ──► banking-mcp server
                                            │
                                            └─ mcp/tools.py
                                               ├─ get_account_balance
                                               ├─ transfer_money
                                               ├─ get_transaction_history
                                               └─ lookup_policy
```

## Tools

### `get_account_balance`

Returns the current and available balance for an account.

```python
get_account_balance(account_id: str) -> BalanceResponse
# Returns: {account_id, balance, currency, available_balance}
# Mock: always returns 50,000,000 VND balance
```

### `transfer_money`

Executes an internal or external bank transfer.

```python
transfer_money(request: TransferRequest) -> TransferResponse
# TransferRequest: {amount, from_account, to_account, recipient_bank}
# Returns: {transaction_id, status, amount, fee, timestamp}
# Mock: fee = 7,000 VND for amounts < 100M; no fee above
```

### `get_transaction_history`

Returns recent transactions for an account.

```python
get_transaction_history(account_id: str, limit: int = 10) -> dict
# Returns: {account_id, transactions: [{id, amount, type, timestamp}, ...]}
# Mock: returns 5 dummy transactions
```

### `lookup_policy`

Answers policy questions about limits, interest rates, and fraud protection.

```python
lookup_policy(question: str) -> str
# Returns a policy string or "Please contact our 24/7 hotline..."
# Mock: keyword-matches "daily limit", "interest rate", "fraud"
```

## Setup

```bash
pip install -r requirements.txt

# Run as standalone MCP server
python -m mcp.server

# Or import and use directly
from mcp.tools import get_account_balance, transfer_money, get_transaction_history, lookup_policy
```

## Requirements

- Python 3.10+
- `mcp>=1.0.0`
- `pydantic>=2.0`

## Testing

```bash
python -m pytest tests/ -v
```

## Dependencies

This package is standalone — no internal dependencies. All other packages are test/runtime only.
