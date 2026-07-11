import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_catalog import is_allowed_live_host, load_catalog, validate  # noqa: E402


class CatalogValidationTests(unittest.TestCase):
    def test_accepts_current_site_hostname_formats(self):
        self.assertTrue(is_allowed_live_host("paper-glider-56.openai.chatgpt.site"))
        self.assertTrue(is_allowed_live_host("project.creator.chatgpt.site"))
        self.assertFalse(is_allowed_live_host("chatgpt.site"))
        self.assertFalse(is_allowed_live_host("example.com"))

    def test_catalog_is_valid(self):
        self.assertEqual(validate(load_catalog(ROOT / "data" / "sites.json")), [])

    def test_invalid_fixture_is_rejected(self):
        records = json.loads((ROOT / "tests" / "fixtures" / "invalid-sites.json").read_text(encoding="utf-8"))
        self.assertTrue(validate(records))


if __name__ == "__main__":
    unittest.main()
