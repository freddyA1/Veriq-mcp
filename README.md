# Veriq MCP

**MCP server for AI agents and businesses to validate emails and phones, look up IPs and domains, and score sign-up fraud risk with one API key.**

Veriq is a hosted (remote) MCP server. Nothing to install: point your MCP client at the endpoint and add your API key.

- Website: https://veriq-u2at.onrender.com
- Agent docs: https://veriq-u2at.onrender.com/agents
- Endpoint (Streamable HTTP): `https://veriq-u2at.onrender.com/mcp/`
- Free key: 250 credits, no card. Paid plans from $19/month.

## Tools

| Tool | What it does |
|---|---|
| `validate_email` | Syntax, typo fixes (gmial.com → gmail.com), disposable and role inboxes, free vs company domain, live MX check |
| `validate_phone` | Valid for its country, E.164 format, line type (mobile, landline, VoIP, toll-free), carrier, timezone |
| `validate_contacts` | Batch check a list of emails and phone numbers in one call |
| `lookup_ip` | Network owner, country, Tor / VPN / data-center flags |
| `lookup_domain` | Domain age, registrar, SPF and DMARC records |
| `score_signup_risk` | Email + phone + IP in one call → 0–100 fraud score, plain-English reasons, and an `agent_action` (accept / ask the user / reject) |

Every result includes an `agent_action` so your agent knows what to do next.

## Setup

1. Get a free API key at https://veriq-u2at.onrender.com
2. Add Veriq to your MCP client.

### Claude Desktop, Cursor, Windsurf, and other clients

```json
{
  "mcpServers": {
    "veriq": {
      "url": "https://veriq-u2at.onrender.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_VERIQ_KEY"
      }
    }
  }
}
```

### Clients that only support stdio

```json
{
  "mcpServers": {
    "veriq": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://veriq-u2at.onrender.com/mcp/", "--header", "Authorization: Bearer YOUR_VERIQ_KEY"]
    }
  }
}
```

## Example

Ask your agent:

> "Before creating this account, check john@gmial.com, +233 20 000 0000 and IP 185.220.101.1."

Veriq suggests the gmail.com fix, checks the phone's line type and carrier, flags the Tor exit node, and returns a risk score with `agent_action: "reject"`.

## Notes

- Email checks go as far as the mail server. Veriq never sends a test message, so it can't confirm a mailbox exists.
- Also available as a REST API: see https://veriq-u2at.onrender.com/agents

## Support

fredrickaffoh81@gmail.com

## Python client

```bash
pip install git+https://github.com/freddyA1/Veriq-mcp
```

```python
from veriq_client import Veriq
v = Veriq()  # reads VERIQ_API_KEY
v.email("jane@gmial.com")["agent_action"]   # "confirm_with_user" (typo for gmail.com)
v.signup_risk(email="x@mailinator.com", ip="185.220.101.1")
```

Architecture: [ARCHITECTURE.md](ARCHITECTURE.md). Data handling: [PRIVACY.md](PRIVACY.md). Security: [SECURITY.md](SECURITY.md).
