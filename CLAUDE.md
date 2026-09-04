# CLAUDE.md — le-veilleur

Read this first; it is the map of how to build, check and operate every part of this repo.

## Context

Automated daily LinkedIn tech-watch. Author: Aurélien Allienne, Engineering Director & GenAI
Architect at SFEIR Lille. The pipeline runs unattended at 06:00 Europe/Paris and publishes to
GitHub Pages; nothing here is meant to require a human on a good day.

## Layout

| Dir | Stack | Manager | Role |
|---|---|---|---|
| `site/` | Astro 5 + Tailwind | `npm` (in `site/`) | The public site. Deployed to Pages on any push touching `site/**`. |
| `minion/` | Python 3.12 + Pydantic | `uv` (in `minion/`) | The pipeline. A standalone uv project, not a workspace member. |
| `infra/` | Terraform | — | Cloud Run Job, Scheduler, IAM, budget kill-switch. |
| `functions/` | Python | — | `budget-killswitch`: the Cloud Function `infra/killswitch.tf` deploys. |
| `scripts/` | bash + Python | root `uv` | Deploy helpers; two local on-demand tools. |
| `linkedin/` | markdown | — | One LinkedIn draft per day, committed by the pipeline. |

Toolchain is pinned in `mise.toml` — run `mise install` once per clone. A root `Justfile` wraps
everything: run `just` for the list. Prefer `just` recipes over calling scripts directly.

## Commands

```bash
just check          # ruff + ruff format + pyright + pytest on minion/ — the same gates CI runs
just test           # pytest only
just test-integration  # pytest -m integration — hits real Claude/Imagen/GitHub; needs the secrets
just build          # astro build — the real content gate (zod validates every frontmatter)
just run [DATE]     # the whole pipeline locally; needs the four secrets in the env
just image          # build the amd64 image and smoke it
just tf-check       # terraform fmt + validate
```

## The nine pipeline steps

`gmail` → `scrape` → `validate_input` → `assemble` → `generate` → `validate_output` → `imagen`
→ `github` → `fiches`

Ordering is fixed by `config.STEP_ORDER`, which is `tuple(StepName)`. `minion/README.md` describes
each step; `minion/src/minion/cli.py` is the composition root and the only place that knows which
adapter is real.

## Invariants worth knowing before you change things

**The site's content schema is the contract.** `site/src/content/config.ts` defines the `articles`,
`blog` and `fiches` collections. `minion/src/minion/publish/serialize.py` must emit exactly those
shapes — if the two drift, `astro build` fails, which is the gate. Fiche frontmatter keys are
**English** (`url`, `authors`, `keywords`, `theme`, `tone`, `used_in`); French keys break the schema.

**Themes are a closed French vocabulary**, defined once in `config.THEME_PRIORITY`:
`IA`, `Leadership`, `Tech`, `Sécurité`, `Data`, `Géopolitique`. Articles carry up to three in
`themes`; fiches carry a single `theme` with `Autre` as the schema default — two different fields,
do not conflate them.

**`sources` is derived, never declared.** `serialize.count_sources` counts the numbered entries
under the body's `## Sources` heading. The model is not asked for the number, so it cannot drift
from what the article actually cites — which means the Sources list format
(`N. [Titre](URL)`, one per line) is load-bearing.

**The `/generate` spec is production code.** `minion/.claude/commands/generate.md` is what the
runtime executes and what ships in the image. `tests/test_generate_contract.py` asserts it agrees
with the Pydantic models, the caps and the theme allowlist — keep them in step.

**`ANTHROPIC_API_KEY` must stay absent.** `secrets.py` raises at import if it is set, and every
`claude` subprocess strips it and injects `CLAUDE_CODE_OAUTH_TOKEN` instead. The API-key path is a
documented break-glass (`infra/RUNBOOK.md` §3c), not a toggle.

**Two container facts that cost a day each to learn:** the image must run as a **non-root** user
(`claude -p --permission-mode bypassPermissions` refuses root), and the Job needs **1Gi** of memory
(512Mi OOM-kills mid-`generate` and leaves no trace, because nothing runs on SIGKILL).

**No datastore.** Run state is in-process; the durable trace is Cloud Logging and the artefacts are
git. A run whose commit fails is lost and must be replayed — `--date` is deterministic, because the
Gmail window is a pure function of the date (the 24h ending at 06:00 Paris).

## Conventions

- **Python**: Pydantic at every I/O boundary; `ruff` lint + format; `pyright` strict; no `print`
  outside the logging boundary. Every external boundary is a `Protocol` in a `*/ports.py` with a
  real adapter and an in-memory double in `fakes.py` — tests are hermetic, no network.
- **Terraform**: `fmt` + `validate` in CI. Secret *slots* are Terraform's; secret *values* never
  are — `scripts/add-secret-versions.sh` adds versions so nothing lands in the state file.
- **Commits**: Conventional Commits. Never `git add .` — stage explicitly.
- **The daily commit is the pipeline's**, on `main`, touching `site/**` and `linkedin/**`. Avoid
  pushing to `site/**` between 06:00 and 06:15 Paris.

## Skills

- `/blog <slug>` — publish a personal blog post to `site/src/content/blog/`. The mascot bible it
  references lives in `minion/.claude/commands/generate.md`; there is deliberately only one copy.
