"""MCP server for banking tools."""

from mcp.server import Server
from mcp.types import Tool, TextContent
from .tools import (
    get_account_balance,
    transfer_money,
    get_transaction_history,
    lookup_policy,
)

server = Server("banking-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_account_balance",
            description="Get the current balance for a bank account",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string", "description": "Account ID"},
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="transfer_money",
            description="Transfer money to another bank account",
            inputSchema={
                "type": "object",
                "properties": {
                    "amount": {"type": "integer", "description": "Amount in VND"},
                    "from_account": {"type": "string"},
                    "to_account": {"type": "string"},
                    "recipient_bank": {"type": "string", "description": "Recipient bank code"},
                },
                "required": ["amount", "from_account", "to_account", "recipient_bank"],
            },
        ),
        Tool(
            name="get_transaction_history",
            description="Get recent transaction history for an account",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="lookup_policy",
            description="Look up banking policy information",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Policy question"},
                },
                "required": ["question"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "get_account_balance":
        result = get_account_balance(arguments["account_id"])
    elif name == "transfer_money":
        result = transfer_money(arguments)
    elif name == "get_transaction_history":
        result = get_transaction_history(arguments["account_id"], arguments.get("limit", 10))
    elif name == "lookup_policy":
        result = {"policy_answer": lookup_policy(arguments["question"])}
    else:
        raise ValueError(f"Unknown tool: {name}")
    return [TextContent(type="text", text=str(result))]