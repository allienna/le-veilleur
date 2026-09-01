# Le Veilleur — task runner. `just` with no argument lists everything.
#
# Two toolchains: npm inside site/ builds the Astro site, uv inside minion/ runs the pipeline.
# The root uv project holds only the local on-demand tooling in scripts/.

default:
    @just --list

# ── Pipeline ──────────────────────────────────────────────────────

# Run the full pipeline locally for DATE (defaults to today). Needs the four secrets in the env.
run DATE="":
    uv --project minion run python -m minion run {{ if DATE == "" { "" } else { "--date " + DATE } }}

# Lint, format-check, type-check and test the pipeline — the same gates CI runs.
check:
    cd minion && uv run ruff check . && uv run ruff format --check . && uv run pyright && uv run pytest

test:
    cd minion && uv run pytest

# Run the gated tests that hit real Claude / Imagen / GitHub (needs the secrets).
test-integration:
    cd minion && uv run pytest -m integration

# ── Container & deploy ────────────────────────────────────────────

# Build the Minion image for linux/amd64 (Cloud Run Jobs are amd64) and smoke it.
image:
    docker buildx build --platform linux/amd64 -t le-veilleur-minion:dev --load minion/
    ./scripts/image-smoke.sh le-veilleur-minion:dev

# Build, push, and bump the Cloud Run Job image.
deploy:
    ./scripts/deploy-minion.sh

# Walk through populating the four Secret Manager secrets.
secrets:
    ./scripts/add-secret-versions.sh

# Execute the deployed Job once for DATE (defaults to today's scheduled behaviour).
run-cloud DATE="":
    gcloud run jobs execute minion --region=europe-west1 --wait \
      {{ if DATE == "" { "" } else { "--args=run,--date," + DATE } }}

# ── Infra ─────────────────────────────────────────────────────────

tf-check:
    terraform -chdir=infra fmt -check -recursive
    terraform -chdir=infra init -backend=false -input=false
    terraform -chdir=infra validate

# ── Site ──────────────────────────────────────────────────────────

# Install deps and start the Astro dev server.
site:
    cd site && npm install && npm run dev

# Build the site. This is the real content gate: zod validates every frontmatter.
build:
    cd site && npm run build

# Copy an image for a blog post into the site.
add-blog-image SLUG FILE:
    mkdir -p site/public/images
    cp "{{ FILE }}" "site/public/images/{{ SLUG }}.png"
    @echo "Image saved to site/public/images/{{ SLUG }}.png"

# ── Local, on-demand ──────────────────────────────────────────────

# Create a NotebookLM notebook from DATE's published article (needs the `nlm` CLI authenticated).
notebook DATE="" *FLAGS="":
    uv run python3 scripts/create_notebook.py {{ if DATE == "" { `date +%Y-%m-%d` } else { DATE } }} {{ FLAGS }}

# Render the Instagram carousel + teaser for DATE into data/output/.
instagram DATE="":
    uv run python3 scripts/generate_instagram.py {{ if DATE == "" { `date +%Y-%m-%d` } else { DATE } }}

instagram-carousel DATE="":
    uv run python3 scripts/generate_instagram.py {{ if DATE == "" { `date +%Y-%m-%d` } else { DATE } }} --carousel-only

# One-time: install the headless browser the Instagram renderer drives.
instagram-setup:
    uv run playwright install chromium
