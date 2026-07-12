# Prompt Provenance

Every entry records one of these provenance states:

- `official-source` - An official source identifies the site and publishes or links its prompt.
- `creator-submitted` - The creator supplied the prompt directly to this project.
- `creator-confirmed` - The creator confirmed an existing public prompt source.
- `source-link-only` - A public source is known, but the prompt is linked rather than reproduced.
- `not-publicly-available` - Reviewers found no public prompt source and make no claim about the prompt's contents.

Every prompt also records one rights state:

- `CC0-1.0` or `CC-BY-4.0` - The prompt is available under the stated license.
- `creator-permission` - Explicit permission is documented.
- `link-only` - No reproduction right is asserted; this repository stores only a link.
- `not-applicable` - No prompt is stored or linked because no public prompt source is available.

The core list does not accept reconstructed, inferred, or result-derived prompts. `Official-source` describes provenance, not a license: unless reuse rights are separately documented, the record must remain `link-only` and the repository must not copy the prompt text.

`not-publicly-available` records must use `prompt_url: null` and `prompt_license: not-applicable`. Their README entry must say `Prompt not publicly available.` A live-site or other public `source_url` records what reviewers inspected, but must not be represented as a prompt source. If a reliable prompt source is later published, the entry can move to the appropriate provenance and rights state after manual review.
