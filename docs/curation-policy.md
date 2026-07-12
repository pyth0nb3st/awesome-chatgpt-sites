# Curation Policy

This project is a curation, not a comprehensive directory. A core entry must:

- Be publicly accessible without a login.
- Use HTTPS on a deployed subdomain ending in `.chatgpt.site`; the `chatgpt.site` documentation apex is not eligible.
- Have a working primary interaction.
- Have either an identifiable prompt source or an explicit `Prompt not publicly available` status.
- Offer meaningful design, functional, educational, or technical value.
- Be more than an unchanged generic starter template.
- Contain no malware, deceptive downloads, spam, or clearly unsafe behavior.
- Be manually opened and tested.
- Have an objective, human-approved description.
- Remain online and usable.

Community projects should normally be public for at least seven days. Official OpenAI showcase projects may be considered immediately. Maintainers may reject entries even when mechanical checks pass.

Human reviewers consider functionality, originality, visual or interaction quality, prompt learning value, and reliability of provenance. A site should satisfy at least four of these five criteria. This internal rubric is not a public score or leaderboard.

A missing public prompt is not itself disqualifying. A community site without one must still be manually tested, satisfy the normal quality bar, record `not-publicly-available` provenance, use `null` for `prompt_url`, and use `not-applicable` for prompt rights. Maintainers must never infer or reconstruct a prompt from the published result. For these records, `source_url` identifies the reviewed live site or another public source; it does not claim to be a prompt source.

A publisher namespace in a `*.chatgpt.site` hostname is not evidence that the matching person or organization created or owns the site. Creator attribution requires a separate public source or direct confirmation.

The initial seed descriptions were drafted with AI assistance and remain provisional until a person completes the [human review checklist](human-review-checklist.md). The repository must not be presented as compliant with the upstream Awesome `Is not AI-generated` requirement until the list has been independently rewritten and curated by people.
