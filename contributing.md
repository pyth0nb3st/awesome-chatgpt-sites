# Contribution Guidelines

Please read the [curation policy](docs/curation-policy.md), [prompt provenance policy](docs/prompt-provenance.md), and [human review checklist](docs/human-review-checklist.md) before contributing. By participating, you agree to the [Code of Conduct](code-of-conduct.md).

## Submitting a Site

Open one pull request per site with the title `Add site: Site Name`.

The site must have:

- A direct, public HTTPS URL whose hostname is `openai.chatgpt.site` or ends in `.openai.chatgpt.site`.
- A working primary interaction that you personally tested.
- An identifiable original prompt source.
- Creator and source attribution where available.
- A short, objective description that starts with an uppercase character and ends with a period.
- A recorded license or creator permission before any complete prompt is copied into this repository.
- A human reviewer who has independently checked the site, source, provenance, and description.

Do not submit affiliate links, tracking redirects, reconstructed prompts, mass-generated candidates, private sites, unchanged generic templates, or sites with deceptive or unsafe behavior.

## Files to Change

Add the entry to both:

- `README.md`, keeping its section alphabetical.
- `data/sites.json`, keeping records sorted by category and then name.

Link-only prompt sources should remain external. Do not add prompt text to the repository unless compatible permission or licensing is documented.

Use this README format:

```markdown
- [Site Name](https://example.openai.chatgpt.site/) - Objective sentence ending in a period, with [prompt and provenance](https://source.example/).
```

## Pull Request Checklist

- [ ] I submitted one site.
- [ ] I tested the live site and its primary interaction.
- [ ] The live link is direct and contains no tracking parameters.
- [ ] I linked the original prompt source and recorded its provenance.
- [ ] I did not copy prompt text without compatible permission or licensing.
- [ ] I added identical metadata to `README.md` and `data/sites.json`.
- [ ] A human reviewer approved the description and curation decision.
- [ ] I ran `npm test` and `python3 scripts/check_links.py --changed-only`.

Maintainers may reject an entry even when every mechanical check passes. Quality is more important than quantity.
