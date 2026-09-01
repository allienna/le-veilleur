# Le Veilleur

A daily tech-watch article, written and published without me.

Every morning at 06:00 Paris a Cloud Run Job pulls the night's newsletters from a dedicated Gmail
inbox, scrapes what they link to, hands the lot to Claude with a versioned spec, generates an
illustration, and commits the article, its hero image and a ready-to-post LinkedIn draft into this
repo. The commit trips GitHub Pages, and the article is live.

**Read it: <https://allienna.github.io/le-veilleur>**

## How it fits together

```
Cloud Scheduler ──06:00 Europe/Paris──▶ Cloud Run Job ("the Minion")
                                              │
       Gmail ──▶ scrape ──▶ validate ──▶ /generate ──▶ Imagen ──▶ commit
                                                                    │
                                              this repo ──▶ Pages ──▶ site
```

Nine steps, each recorded to Cloud Logging. The commit *is* the publication: there is no database
in the loop, so git is the record and a replay is `--date YYYY-MM-DD`.

| Directory | What it is |
|---|---|
| `site/` | The Astro site — 92 articles, 411 source fiches, a blog. Deployed to Pages on any push touching it. |
| `minion/` | The pipeline: a deterministic Python state machine that shells out to the `claude` CLI for the creative steps. See [`minion/README.md`](minion/README.md). |
| `infra/` | Terraform for the Job, the scheduler, the IAM and a budget kill-switch. Operate it with [`infra/RUNBOOK.md`](infra/RUNBOOK.md). |
| `linkedin/` | One LinkedIn draft per day — the actual daily deliverable, versioned so it is readable from a phone. |
| `scripts/` | Deploy helpers, plus two local on-demand tools (a NotebookLM driver, an Instagram renderer). |

## Getting started

```bash
mise install          # node, uv, just
just --list           # every task
just site             # the site, locally
just check            # the pipeline's gates: ruff, pyright, pytest
```

Running the pipeline itself needs four secrets — a Gmail refresh token, a Claude Code OAuth token,
a GitHub PAT and a Gemini API key. `just secrets` walks through provisioning them; `just run` then
executes the whole thing locally, no GCP credentials required.

## Costs

Around 5 €/month of GCP, plus roughly 0.60 €/month of Imagen. Text generation runs on a Claude Max
subscription through an OAuth token rather than a metered API key, so it costs nothing per run. A
budget kill-switch pauses the scheduler if the bill ever runs away.

## Where this came from

Two earlier projects, merged. [`veilleur`](https://github.com/allienna/veilleur) had the site and a
Claude Code workflow I drove by hand, tied to a local n8n container that had to be running.
[`veilleur-app`](https://github.com/allienna/veilleur-app) had the cloud pipeline, wrapped in a
supervision PWA, a Firestore, a trigger service and a schema-codegen workspace.

This repo keeps the site and the pipeline and drops the rest. Both originals stay online: the old
Pages URLs still resolve, so links already shared on LinkedIn keep working.

---

*The articles are written with AI assistance. The source selection, the editorial line and the
review are mine.*
