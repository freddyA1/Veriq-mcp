import io
import json
import unittest
import urllib.error
from unittest import mock

from veriq_client import Veriq, VeriqError


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def capture(payload):
    calls = []

    def fake_urlopen(req, timeout=None):
        calls.append(req)
        return FakeResp(json.dumps(payload).encode())

    return calls, fake_urlopen


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.v = Veriq(api_key="vq_test", base_url="https://example.test/")

    def test_requires_key(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(ValueError):
                Veriq()

    def test_email_sends_auth_and_body(self):
        calls, fake = capture({"agent_action": "confirm_with_user", "credits_remaining": 249})
        with mock.patch("urllib.request.urlopen", fake):
            out = self.v.email("jane@gmial.com")
        req = calls[0]
        self.assertEqual(req.full_url, "https://example.test/v1/email")
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.get_header("Authorization"), "Bearer vq_test")
        self.assertEqual(json.loads(req.data), {"email": "jane@gmial.com", "check_dns": True})
        self.assertEqual(out["agent_action"], "confirm_with_user")

    def test_none_fields_dropped(self):
        calls, fake = capture({})
        with mock.patch("urllib.request.urlopen", fake):
            self.v.signup_risk(email="a@b.co")
        self.assertEqual(json.loads(calls[0].data), {"email": "a@b.co"})

    def test_signup_risk_needs_input(self):
        with self.assertRaises(ValueError):
            self.v.signup_risk()

    def test_batch_limit(self):
        with self.assertRaises(ValueError):
            self.v.batch(["a@b.co"] * 101)

    def test_account_is_get(self):
        calls, fake = capture({"credits": 250})
        with mock.patch("urllib.request.urlopen", fake):
            self.v.account()
        self.assertEqual(calls[0].get_method(), "GET")
        self.assertIsNone(calls[0].data)

    def test_http_error_raises_with_agent_action(self):
        body = json.dumps({"detail": {"error": "insufficient_credits", "agent_action": "stop_and_tell_user"}})
        err = urllib.error.HTTPError("u", 402, "Payment Required", {}, io.BytesIO(body.encode()))
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(VeriqError) as cm:
                self.v.phone("+233200000000")
        self.assertEqual(cm.exception.status, 402)
        self.assertEqual(cm.exception.agent_action, "stop_and_tell_user")


class ManifestTests(unittest.TestCase):
    def test_server_json(self):
        with open("server.json") as f:
            m = json.load(f)
        for k in ("name", "version", "description", "remotes"):
            self.assertIn(k, m)
        r = m["remotes"][0]
        self.assertEqual(r["type"], "streamable-http")
        self.assertTrue(r["url"].startswith("https://"))
        self.assertTrue(any(h["name"] == "Authorization" and h["isSecret"] for h in r["headers"]))


if __name__ == "__main__":
    unittest.main()
