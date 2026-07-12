import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_readme_sync import parse_entry  # noqa: E402


class ReadmeEntryParsingTests(unittest.TestCase):
    def test_parses_entry_with_public_prompt(self):
        line = (
            "- [Material Lab](https://interactive-studies-56.openai.chatgpt.site/material-lab/) "
            "- Real-time material tool, with [prompt and provenance]"
            "(https://developers.openai.com/showcase/material-lab)."
        )
        self.assertEqual(
            parse_entry(line),
            (
                "Material Lab",
                "https://interactive-studies-56.openai.chatgpt.site/material-lab/",
                "Real-time material tool.",
                "https://developers.openai.com/showcase/material-lab",
            ),
        )

    def test_parses_entry_without_public_prompt(self):
        line = (
            "- [Sumi](https://sumi-ascii.wmoto-ai.chatgpt.site/) - A local image-to-ASCII terminal. "
            "Prompt not publicly available."
        )
        self.assertEqual(
            parse_entry(line),
            (
                "Sumi",
                "https://sumi-ascii.wmoto-ai.chatgpt.site/",
                "A local image-to-ASCII terminal.",
                None,
            ),
        )

    def test_rejects_unmarked_missing_prompt(self):
        self.assertIsNone(
            parse_entry(
                "- [Sumi](https://sumi-ascii.wmoto-ai.chatgpt.site/) - A local image-to-ASCII terminal."
            )
        )


if __name__ == "__main__":
    unittest.main()
