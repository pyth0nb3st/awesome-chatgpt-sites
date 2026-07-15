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

    def test_accepts_prompt_not_publicly_available_state(self):
        record = dict(next(record for record in load_catalog(ROOT / "data" / "sites.json") if record["prompt_url"]))
        record.update(
            {
                "slug": "no-public-prompt",
                "name": "No Public Prompt",
                "prompt_url": None,
                "prompt_provenance": "not-publicly-available",
                "prompt_license": "not-applicable",
            }
        )
        self.assertEqual(validate([record]), [])

    def test_rejects_inconsistent_prompt_availability_state(self):
        record = dict(next(record for record in load_catalog(ROOT / "data" / "sites.json") if record["prompt_url"]))
        record.update(
            {
                "prompt_provenance": "not-publicly-available",
                "prompt_license": "link-only",
            }
        )
        errors = validate([record])
        self.assertTrue(any("requires a null prompt_url" in error for error in errors))
        self.assertTrue(any("requires not-applicable rights" in error for error in errors))

    def test_rejects_not_applicable_rights_for_public_prompt(self):
        record = dict(next(record for record in load_catalog(ROOT / "data" / "sites.json") if record["prompt_url"]))
        record.update({"prompt_url": None, "prompt_license": "not-applicable"})
        errors = validate([record])
        self.assertTrue(any("prompt_url must be an absolute HTTPS URL" in error for error in errors))
        self.assertTrue(any("not-applicable rights require" in error for error in errors))

    def test_invalid_fixture_is_rejected(self):
        records = json.loads((ROOT / "tests" / "fixtures" / "invalid-sites.json").read_text(encoding="utf-8"))
        self.assertTrue(validate(records))


if __name__ == "__main__":
    unittest.main()
