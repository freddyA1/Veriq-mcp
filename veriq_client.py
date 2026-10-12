"""Veriq Python client: email, phone, IP, domain checks and sign-up fraud scoring.

Zero dependencies (standard library only). Get a free key with 250 credits at
https://veriq-u2at.onrender.com
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

__all__ = ["Veriq", "VeriqError"]
__version__ = "0.1.0"

DEFAULT_BASE_URL = "https://veriq-u2at.onrender.com"


class VeriqError(Exception):
    """Raised when the API returns an error. `status` is the HTTP code, `detail` the parsed body."""

    def __init__(self, status: int, detail: Any):
        self.status = status
        self.detail = detail
        super().__init__(f"Veriq API error {status}: {detail}")

    @property
    def agent_action(self) -> str | None:
        d = self.detail.get("detail", self.detail) if isinstance(self.detail, dict) else None
        return d.get("agent_action") if isinstance(d, dict) else None


class Veriq:
    """Thin client for the hosted Veriq REST API.

    >>> v = Veriq()                      # reads VERIQ_API_KEY
    >>> v.email("jane@gmial.com")["agent_action"]
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 20.0):
        self.api_key = api_key or os.environ.get("VERIQ_API_KEY", "")
        if not self.api_key:
            raise ValueError("Pass api_key or set VERIQ_API_KEY (free key at https://veriq-u2at.onrender.com)")
        self.base_url = (base_url or os.environ.get("VERIQ_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout

    # --- transport ---
    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        data = None if body is None else json.dumps({k: v for k, v in body.items() if v is not None}).encode()
        req = urllib.request.Request(
            self.base_url + path, data=data, method=method,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json",
                     "User-Agent": "veriq-client-python/0.1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            raw = e.read().decode(errors="replace")
            try:
                detail = json.loads(raw)
            except ValueError:
                detail = raw
            raise VeriqError(e.code, detail) from None

    # --- endpoints (credits per call in brackets) ---
    def email(self, email: str, check_dns: bool = True) -> dict:
        """[1] Syntax, typo suggestion, disposable, role account, MX."""
        return self._request("POST", "/v1/email", {"email": email, "check_dns": check_dns})

    def phone(self, phone: str, default_country: str | None = None) -> dict:
        """[1] E.164, validity, line type, carrier region. default_country is ISO alpha-2 (GH, US)."""
        return self._request("POST", "/v1/phone", {"phone": phone, "default_country": default_country})

    def validate(self, value: str, default_country: str | None = None) -> dict:
        """[1] Auto-detects email or phone."""
        return self._request("POST", "/v1/validate", {"value": value, "default_country": default_country})

    def batch(self, values: list[str], default_country: str | None = None, check_dns: bool = True) -> dict:
        """[1 each] Up to 100 emails and/or phones in one call."""
        if len(values) > 100:
            raise ValueError("batch accepts at most 100 values; split the list")
        return self._request("POST", "/v1/batch",
                             {"values": values, "default_country": default_country, "check_dns": check_dns})

    def ip(self, ip: str) -> dict:
        """[1] ASN, network owner, country, Tor / VPN / data-center flags."""
        return self._request("POST", "/v1/ip", {"ip": ip})

    def domain(self, domain: str) -> dict:
        """[2] Domain age, registrar, mail provider, SPF / DMARC."""
        return self._request("POST", "/v1/domain", {"domain": domain})

    def signup_risk(self, email: str | None = None, phone: str | None = None, ip: str | None = None,
                    default_country: str | None = None) -> dict:
        """[3] One fraud score for a sign-up or lead from any of email, phone, IP."""
        if not (email or phone or ip):
            raise ValueError("send at least one of email, phone, ip")
        return self._request("POST", "/v1/signup-risk",
                             {"email": email, "phone": phone, "ip": ip, "default_country": default_country})

    def account(self) -> dict:
        """[0] Plan and credits remaining."""
        return self._request("GET", "/v1/account")
