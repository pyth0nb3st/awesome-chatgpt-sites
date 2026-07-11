# Human Review Checklist

The current seed catalog was assembled with AI assistance and is not upstream-ready. A human maintainer must complete this checklist for every record before changing `reviewed_by_human` to `true`.

- [ ] Open the exact live URL in a normal browser without a login.
- [ ] Exercise the primary interaction on desktop or mobile.
- [ ] Confirm the final URL remains on an allowed hostname.
- [ ] Open the source URL and verify it identifies the same site.
- [ ] Confirm the stated prompt provenance and rights status.
- [ ] Confirm no unlicensed prompt text is stored locally and every local preview has a source and rights record.
- [ ] Independently assess functionality, originality, quality, learning value, and provenance reliability.
- [ ] Rewrite or explicitly approve the description without relying on AI output.
- [ ] Confirm the description is objective, starts uppercase, and ends with a period.
- [ ] Record the reviewer and review date in the pull request discussion.

Before any submission to `sindresorhus/awesome`, people must also re-curate the list, confirm it is not AI-generated, wait at least 30 days from the later of the first real commit or public release, review the current upstream requirements, and run `awesome-lint` without bypassing failures.
