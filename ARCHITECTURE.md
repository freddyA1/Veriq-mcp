# Architecture

Veriq is a hosted API. This repository holds the public integration layer: the MCP manifest, an open-source Python client, and its tests. The verification engine runs as a managed service and is not open source.

```
AI agent / MCP client ──Streamable HTTP──▶ https://veriq-u2at.onrender.com/mcp/  ┐
Your backend ──veriq_client / REST──────▶ https://veriq-u2at.onrender.com/v1/*  ┴▶ Veriq engine
```

## What's in this repo

| Path | Purpose |
| --- | --- |
| `server.json` | MCP registry manifest: remote endpoint, transport, required `Authorization` header |
| `veriq_client.py` | Zero-dependency Python client for the REST API |
| `test_veriq_client.py` | Unit tests for the client and manifest, run in CI on every push |

## Interfaces

Both interfaces use the same API key and credit balance.

| MCP tool | REST endpoint | Credits |
| --- | --- | --- |
| `validate_email` | `POST /v1/email` | 1 |
| `validate_phone` | `POST /v1/phone` | 1 |
| `validate_contacts` | `POST /v1/batch` (max 100) | 1 each |
| `lookup_ip` | `POST /v1/ip` | 1 |
| `lookup_domain` | `POST /v1/domain` | 2 |
| `score_signup_risk` | `POST /v1/signup-risk` | 3 |

Every result carries an `agent_action` (`accept`, `confirm_with_user`, `reject_if_signup_else_confirm`, or `reject`) and plain-English reasons, so an agent can act without parsing raw fields.

## Errors

| Status | Meaning | `agent_action` |
| --- | --- | --- |
| 401 | Missing or invalid key | `stop_and_tell_user` |
| 402 | Out of credits | `stop_and_tell_user` |
| 429 | Rate limited | retry after `retry_after_seconds` |

## Data sources

Email checks use syntax rules, disposable and role lists, and live DNS/MX. Phone checks use numbering-plan metadata. IP checks use public routing data (ASN) and the Tor exit list. Domain checks use RDAP plus SPF and DMARC records. See [PRIVACY.md](PRIVACY.md) for what is and isn't stored.
