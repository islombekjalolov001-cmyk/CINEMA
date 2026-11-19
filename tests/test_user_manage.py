import unittest

from handlers.admin.panel import format_user_reference, normalize_user_identifier
from keyboards.inline.subscribe import build_subscribe_url
from services.subscription import normalize_channel_reference


class ChannelAndUserHelpersTests(unittest.TestCase):
    def test_normalize_user_identifier(self):
        self.assertEqual(normalize_user_identifier(" @demo_user "), "demo_user")
        self.assertEqual(normalize_user_identifier(" 12345 "), "12345")

    def test_format_user_reference(self):
        user = {"user_id": 42, "username": "demo", "full_name": "Demo User"}
        text = format_user_reference(user)
        self.assertIn("42", text)
        self.assertIn("demo", text)
        self.assertIn("Demo User", text)

    def test_normalize_public_channel_references(self):
        self.assertEqual(normalize_channel_reference("https://t.me/filmkanal"), "@filmkanal")
        self.assertEqual(normalize_channel_reference("t.me/filmkanal"), "@filmkanal")
        self.assertEqual(normalize_channel_reference("https://telegram.me/filmkanal"), "@filmkanal")
        self.assertEqual(normalize_channel_reference("@filmkanal"), "@filmkanal")
        self.assertEqual(normalize_channel_reference("https://t.me/kinoman_000"), "@kinoman_000")
        self.assertEqual(normalize_channel_reference("https://t.me/+invite"), "")

    def test_subscribe_url(self):
        self.assertEqual(build_subscribe_url("@filmkanal"), "https://t.me/filmkanal")
        self.assertEqual(build_subscribe_url("https://example.com"), "https://example.com")


if __name__ == "__main__":
    unittest.main()
