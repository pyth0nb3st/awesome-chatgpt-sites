import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_catalog import load_catalog, validate  # noqa: E402


class CatalogValidationTests(unittest.TestCase):
    def test_catalog_is_valid(self):
        self.assertEqual(validate(load_catalog(ROOT / "data" / "sites.json")), [])

    def test_invalid_fixture_is_rejected(self):
        records = json.loads((ROOT / "tests" / "fixtures" / "invalid-sites.json").read_text(encoding="utf-8"))
        self.assertTrue(validate(records))


if __name__ == "__main__":
    unittest.main()
