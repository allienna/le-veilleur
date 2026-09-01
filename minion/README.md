# minion

The daily pipeline: a deterministic Python state machine that shells out to the `claude` CLI for
the creative steps, packaged as a one-shot Cloud Run Job.

```bash
uv sync
uv run python -m minion run --date 2026-09-01   # defaults to today
```

## The nine steps

| # | Step | What it does |
|---|---|---|
| 1 | `gmail` | Pull newsletters from the dedicated inbox over the 24h ending at 06:00 Paris of the run date. Extracts and de-duplicates candidate links. |
| 2 | `scrape` | Fetch each URL from its origin (`httpx`, browser-like UA) and extract main content to Markdown with `trafilatura`, in-process. Detects paywalls from the raw HTML. |
| 3 | `validate_input` | Empty mailbox → graceful `skipped/no_sources`. Otherwise require ≥5 sources OK **and** ≥50% of candidates. |
| 4 | `assemble` | De-duplicate by title (syndication guard) and trim to the input-token budget. |
| 5 | `generate` | `claude -p "/generate <context.json>"` → one JSON artefact: theme, frontmatter, body, LinkedIn post, image prompt. |
| 6 | `validate_output` | The deterministic gate of record: length caps, frontmatter completeness, and the copyright rules. Failures are fed back and `/generate` is re-invoked. |
| 7 | `imagen` | Imagen 4 Fast via the Gemini API → PNG. On a moderation block: one softened rewrite, then ship without an image. |
| 8 | `github` | Commit the image, the article markdown and the LinkedIn post through the GitHub Contents API. |
| 9 | `fiches` | One per-source analysis per *cited* source, committed to the site. Non-blocking by design. |

Each step records `running` → terminal with timestamps; a raising step halts the run. A step may
also end the run gracefully (`skipped`) or latch a warning that downgrades the final status to
`success_with_warnings`.

## Design

Hexagonal: every external boundary is a `Protocol` in a `*/ports.py`, with a production adapter
and an in-memory double in `fakes.py`. The whole pipeline therefore runs hermetically in tests —
no Gmail, no Claude, no Imagen, no GitHub, no network.

Run state is in-process only (`store/memory.py`): the job is one-shot, its durable trace is Cloud
Logging, and the published artefacts live in the repo, where git is the record.

`cli.py` is the composition root and the only place that knows which adapter is real.

## Secrets

Read at run time from Secret Manager (or plain environment variables locally):
`gmail-oauth-refresh-token`, `anthropic-oauth-token`, `github-pat`, `gemini-api-key`.

`ANTHROPIC_API_KEY` is deliberately absent — `secrets.py` raises at import if it is set. The
agentic steps authenticate with `CLAUDE_CODE_OAUTH_TOKEN` only.

## Checks

```bash
uv run ruff check . && uv run ruff format --check .
uv run pyright
uv run pytest                  # hermetic
uv run pytest -m integration   # hits real Claude / Imagen / GitHub; needs the secrets
```

## Container

Build context is this directory, and the image **must** be amd64 (Cloud Run Jobs are amd64):

```bash
docker buildx build --platform linux/amd64 -t le-veilleur-minion:dev minion/
../scripts/image-smoke.sh le-veilleur-minion:dev
```

Two container invariants worth remembering: the image runs as a **non-root** user (`claude -p
--permission-mode bypassPermissions` refuses to run as root), and the Cloud Run Job needs
**1Gi** of memory — 512Mi OOM-kills mid-`generate` and leaves no trace, because nothing runs on
SIGKILL.
