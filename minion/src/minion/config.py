"""Static configuration constants for the Minion orchestrator.

Module-level constants only — no side effects, no I/O. The 20-minute run timeout is not
enforced in-process; the Cloud Run Job `timeout` is the real ceiling (infra/job.tf) and this
constant reuses it as the stale-lock TTL.
"""

from __future__ import annotations

from datetime import timedelta
from zoneinfo import ZoneInfo

from minion.models import StepName

# Wall-clock ceiling for a single run. Reused as the lock-staleness TTL.
RUN_TIMEOUT: timedelta = timedelta(minutes=20)

# All run timestamps and the daily date key are computed in this zone (PRD: Europe/Paris).
PARIS_TZ: ZoneInfo = ZoneInfo("Europe/Paris")


# The ten canonical pipeline steps, in execution order (the StepName enum is declaration
# ordered to match the pipeline).
STEP_ORDER: tuple[StepName, ...] = tuple(StepName)

# --- Ingestion ---------------------------------------------------------------------------

# Secret holding the operator's Gmail OAuth refresh-token JSON (authorized_user.json shape).
GMAIL_REFRESH_TOKEN_SECRET: str = "gmail-oauth-refresh-token"

# Read-only Gmail access — the pipeline never marks messages read, which keeps replay
# idempotent and avoids the broader gmail.modify scope.
GMAIL_SCOPES: tuple[str, ...] = ("https://www.googleapis.com/auth/gmail.readonly",)

# Sender denylist. Empty, maintained manually. An entry matches a newsletter
# when it equals the full From address (case-insensitive) or is an "@domain" suffix of it.
EXCLUDED_SENDERS: frozenset[str] = frozenset()

# Per-run hard caps. Truncation is logged, never silent.
MAX_NEWSLETTERS: int = 50
MAX_URLS: int = 100

# Substrings signalling paywalled content, matched against the origin server's raw HTML —
# before trafilatura runs, since extraction may strip the paywall notice itself. The strongest
# signal is the schema.org JSON-LD `isAccessibleForFree:false` many publishers embed; the rest
# are common visible paywall CTAs. A starter set, conservative by design: a false positive
# wrongly drops a good source. Refine it against captured HTML as failures show up.
PAYWALL_MARKERS: tuple[str, ...] = (
    '"isAccessibleForFree":false',
    '"isAccessibleForFree": false',
    "This content is for subscribers only",
    "Subscribe to continue reading",
    "Subscribe to read",
    "Already a subscriber",
)

# --- Scrape / local extraction -----------------------------------------------------------
# Each candidate URL is fetched directly from its origin (httpx, browser-like UA + redirects),
# then main content is extracted in-process by trafilatura. No external scraping service / key /
# rate limit.

# Browser-like UA — many publishers 403 a bare/library client.
SCRAPE_USER_AGENT: str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
SCRAPE_TIMEOUT: timedelta = timedelta(seconds=30)  # per-request HTTP timeout
SCRAPE_MAX_RETRIES: int = 2  # retries after the first attempt on transient errors
SCRAPE_BACKOFF_BASE: timedelta = timedelta(seconds=1)  # exponential backoff unit
# Bounded fetch-pool concurrency — politeness per-origin, not central-throttle avoidance.
SCRAPE_WORKERS: int = 6
# Minimum spacing between requests to the *same host* (2026-08-02 burn-in: newsletters that
# link dozens of posts on one host — e.g. Substack, or a tracking-redirect domain like Beehiiv's
# link.mail.beehiiv.com — got 6 workers hitting that host at once, tripping its own rate limiter
# (429/403) even though SCRAPE_WORKERS caps *global* concurrency, not per-host.
SCRAPE_HOST_MIN_INTERVAL: timedelta = timedelta(seconds=2)
# Overall scrape budget — roughly 3 min in practice, and it must not eat the run's 20.
SCRAPE_DEADLINE: timedelta = timedelta(minutes=4)

# Input-validation threshold: continue only if ≥50% of candidates scraped OK AND
# ≥5 sources OK; otherwise the run hard-fails.
MIN_SOURCES_OK: int = 5
MIN_SOURCES_FRACTION: float = 0.5

# --- Generation / `/generate` ------------------------------------------------------------

# Secret holding the Claude Code OAuth token (`claude setup-token`). The generate subprocess
# authenticates via this; ANTHROPIC_API_KEY is stripped from its env.
ANTHROPIC_OAUTH_TOKEN_SECRET: str = "anthropic-oauth-token"

# The agentic invocation. `/generate` is vendored at .claude/commands/generate.md and copied
# into the image, so the runtime executes a spec that ships with it.
CLAUDE_CMD: tuple[str, ...] = (
    "claude",
    "-p",
    "/generate",
    "--permission-mode",
    "bypassPermissions",
    # JSON envelope on stdout so the runner can read `total_cost_usd` + `usage` alongside the
    # artefact `result`, which is what the run logs report as cost/tokens.
    "--output-format",
    "json",
)
CLAUDE_TIMEOUT: timedelta = timedelta(minutes=8)  # ~4 min typical, 8 is the ceiling
CLAUDE_BACKOFF_BASE: timedelta = timedelta(seconds=2)  # transport-retry backoff unit
# Retry budget is bounded by the 20-minute hard run timeout: a real `/generate` on a
# dense multi-source day takes ~6-7 min, so the generate loop must fit <=2 invocations to clear
# end-to-end (scrape + Imagen + GitHub) inside 20 min. Lowered from 2 after real runs.
CLAUDE_TRANSPORT_RETRIES: int = 1  # retries on a Claude transport error, distinct from validation

# Per-run caps. Token budgets use a char heuristic, not a
# real tokenizer — a guard, not an exact bound.
MAX_GENERATE_INPUT_TOKENS: int = 500_000
MAX_GENERATE_OUTPUT_TOKENS: int = 30_000
MAX_ARTICLE_WORDS: int = 10_000
MAX_LINKEDIN_CHARS: int = 3000
MAX_IMAGE_PROMPT_CHARS: int = 1000

# Astro article frontmatter. Source of truth is site/src/content/config.ts — the `articles`
# collection: title (str), date (coerced), themes (str[]), sources (int), image (str).
# `sources` is derived from the body, not asked of the model, so it is not required here.
REQUIRED_FRONTMATTER_FIELDS: tuple[str, ...] = ("title", "date", "themes")

# The theme vocabulary actually in use on the site, French and capitalized. Ordered most- to
# least-frequent; `THEME_PRIORITY` breaks ties when capping an article at MAX_THEMES.
THEME_PRIORITY: tuple[str, ...] = ("IA", "Leadership", "Tech", "Sécurité", "Data", "Géopolitique")
THEME_ALLOWLIST: frozenset[str] = frozenset(THEME_PRIORITY)
DEFAULT_THEME: str = "Tech"  # unknown theme normalizes here — not an error
MAX_THEMES: int = 3  # ArticleCard renders at most three pills

# Copyright post-validator. These thresholds were recalibrated against real 47-source days:
# the original, stricter values fired on non-infringing content — a product name ("Large
# Industry Model") counted as a quote, and a single 12-token run of generic French prose counted
# as "wholesale". The rules exist to bar *substantial* verbatim quoting and passage-level
# copying, not proper nouns or stock phrasing.
MAX_QUOTE_WORDS: int = 30  # max words in a single direct quote per source
MAX_QUOTES_PER_SOURCE: int = 1  # max distinct substantial quotes attributable to one source
# A quoted span counts toward MAX_QUOTES_PER_SOURCE only at/above this length — short spans are
# product names / labels / emphasis, not copyrightable excerpts.
MIN_COUNTED_QUOTE_WORDS: int = 6
WHOLESALE_NGRAM: int = 20  # ≥ this many consecutive shared tokens ⇒ wholesale reproduction

# Agentic validation-retry budget: re-invoke `/generate` with the errors fed back. Lowered
# 2 -> 1 so the generate loop (<=2 invocations, ~6-7 min each) plus scrape + Imagen + GitHub fits
# the 20-minute run timeout; the job timeout is the backstop.
MAX_GENERATE_RETRIES: int = 1

# --- Publish: Imagen + GitHub ------------------------------------------------------------

# Image generation via the Gemini API (an API key, not GCP IAM) — so the pipeline also runs
# locally without GCP credentials. There is no Imagen model behind a Developer API key (only
# behind Vertex IAM or a Gemini Enterprise-tied key); the reachable model family is the Gemini
# multimodal "image" models, called through generate_content, not generate_images/predict.
# gemini-2.5-flash-image returns PNG bytes natively in this mode — the newer 3.1 family defaults
# to JPEG and Developer API keys cannot override that (output_mime_type is Enterprise-only).
GEMINI_API_KEY_SECRET: str = "gemini-api-key"
IMAGE_MODEL: str = "gemini-2.5-flash-image"
IMAGEN_ASPECT_RATIO: str = "16:9"  # every hero image is 16:9
# One agentic prompt-rewrite retry on a moderation rejection before giving up on the image.
IMAGEN_RETRIES: int = 1
# The Le Veilleur brand template appended to the article's image_prompt. Keeps the mascot
# on-brand and moderation-safe even if the model's own prompt drifts.
IMAGEN_BRAND_TEMPLATE: str = (
    "Featuring the mascot 'Le Veilleur' — a cartoon owl with navy plumage, large amber eyes, "
    "friendly Pixar 3D style, soft studio lighting. 16:9 aspect ratio."
)

# GitHub Contents API target — this very repo. The Minion runs in Cloud Run with no checkout,
# so it publishes through the API; the commit lands on `site/**` and trips the Pages workflow.
GITHUB_PAT_SECRET: str = "github-pat"
GITHUB_REPO_OWNER: str = "allienna"
GITHUB_REPO_NAME: str = "le-veilleur"
GITHUB_BRANCH: str = "main"
# Keyed by date alone: one article per day, and a replay overwrites rather than duplicating.
POST_MD_PATH_TEMPLATE: str = "site/src/content/articles/{date}.md"
POST_IMAGE_PATH_TEMPLATE: str = "site/public/images/{date}.png"
FICHE_MD_PATH_TEMPLATE: str = "site/src/content/fiches/{date}-{slug}.md"
# The LinkedIn post is the real daily deliverable. Outside site/, so it is versioned and
# readable from a phone without being published.
LINKEDIN_PATH_TEMPLATE: str = "linkedin/{date}.md"
GITHUB_TIMEOUT: timedelta = timedelta(seconds=30)  # per-request HTTP timeout
GITHUB_RETRIES: int = 3  # retries after the first attempt on a commit failure
GITHUB_BACKOFF_BASE: timedelta = timedelta(seconds=1)  # exponential backoff unit

# Slug derivation from a source title (fiches only — articles are keyed by date).
# Length-capped, URL-safe.
SLUG_MAX_LEN: int = 80

# Run-level warning latched when Imagen could not be satisfied. No placeholder asset is
# committed: the frontmatter simply omits `image` and the site's layouts fall back to
# public/images/placeholder-veilleur.svg on their own.
IMAGEN_FALLBACK_WARNING: str = "imagen_unavailable"

# --- Fiches: per-source analysis ---------------------------------------------------------
# Non-blocking by design: a failed fiche is skipped, never a run failure. Placed last in
# STEP_ORDER, after the commit, so it can never prevent the article itself from shipping.

# Shorter than CLAUDE_TIMEOUT: one source's markdown, not the whole assembled context.
FICHE_TIMEOUT: timedelta = timedelta(minutes=4)
FICHE_TRANSPORT_RETRIES: int = 1
FICHE_BACKOFF_BASE: timedelta = timedelta(seconds=2)
# IO-bound `claude` subprocess calls, run concurrently so N cited sources don't cost N times the
# per-call wall-clock time end to end.
FICHE_MAX_CONCURRENCY: int = 3
# Calibrated against the 411 fiches already on the site (median 744 words, p90 1413,
# max 5198): `## Analyse approfondie` is an *integral* French translation of the source,
# not a summary, so long sources legitimately run long. 1500 would have rejected 8% of
# the existing corpus. This is a runaway-output guard, not an editorial limit.
MAX_FICHE_WORDS: int = 6000
