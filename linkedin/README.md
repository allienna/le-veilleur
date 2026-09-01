# linkedin/

One file per day, `YYYY-MM-DD.md`, holding the LinkedIn post the pipeline wrote for that day's
article. Plain text, no frontmatter, no heading: the whole file is meant to be selected and pasted
into LinkedIn.

The `github` step commits these alongside the article. They live outside `site/` on purpose — the
post is a draft to publish by hand, not something the site should serve — but they are versioned,
so they are readable from a phone, survive a lost laptop, and can be fed to
`scripts/generate_instagram.py`.

In the veilleur-app PoC this text was written to Firestore for the PWA to read. With no PWA it had
nowhere to go, which would have quietly dropped the pipeline's actual daily deliverable.
