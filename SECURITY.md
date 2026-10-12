# Security policy

Report vulnerabilities privately to **fredrickaffoh81@gmail.com** with "SECURITY" in the subject. Please don't open a public issue.

Include what you found, steps to reproduce, and the impact. You'll get an acknowledgement within 72 hours and an update when it's fixed. Good-faith research that avoids other users' data and service disruption won't be pursued.

In scope: the hosted API and MCP endpoint at `veriq-u2at.onrender.com`, and the code in this repo.

For integrators:
- Keep API keys in environment variables (`VERIQ_API_KEY`), never in code or commits.
- Keys are stored hashed server-side; if one leaks, rotate it from your dashboard.
- All traffic is HTTPS only.
