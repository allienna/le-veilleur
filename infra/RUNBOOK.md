# Le Veilleur — operations runbook

Operational procedures for bringing up and running the Minion in production. These steps need
**live GCP credentials** and are run by the operator — they are **not** part of CI.

> **Account precondition (every step):** the active gcloud account MUST be the personal
> `aurelien.allienne@gmail.com` on project `veilleur-app` — **not** the Adeo work account. The
> CLI identity flips back silently; pass `--account=aurelien.allienne@gmail.com` or
> `gcloud config set account aurelien.allienne@gmail.com` first.

## 0. Adopt the resources that already exist (do this first, once)

The GCP project already holds resources created by the veilleur-app PoC's separate Terraform
state. This root declares them too, so a first `apply` would try to create them again and fail
with "already exists". Import them instead:

```bash
terraform -chdir=infra init

# The two secrets provisioned for the PoC (the other two are new — let Terraform create them).
terraform -chdir=infra import \
  'google_secret_manager_secret.runtime["gmail-oauth-refresh-token"]' \
  projects/veilleur-app/secrets/gmail-oauth-refresh-token
terraform -chdir=infra import \
  'google_secret_manager_secret.runtime["anthropic-oauth-token"]' \
  projects/veilleur-app/secrets/anthropic-oauth-token

# The image repo.
terraform -chdir=infra import google_artifact_registry_repository.minion \
  projects/veilleur-app/locations/europe-west1/repositories/minion

# Already-enabled APIs, one per service, e.g.:
terraform -chdir=infra import 'google_project_service.enabled["run.googleapis.com"]' \
  veilleur-app/run.googleapis.com
```

Then `terraform -chdir=infra plan` and read it carefully: it must show **no destroys**. A plan
proposing to destroy a secret means an import was missed — stop and import it. The old PoC state,
if you still have it, must never be applied again against this project.

## 1. First-time bring-up

```bash
# 0. Auth (personal account + project)
gcloud config set account aurelien.allienne@gmail.com
gcloud config set project veilleur-app

# 1. Populate the Secret Manager versions (the slots are created by Terraform)
./scripts/add-secret-versions.sh   # gmail refresh token, anthropic OAuth token, github PAT, gemini key

# 2. Push the first image (the Job cannot be created without one)
terraform -chdir=infra apply -target=google_artifact_registry_repository.minion
./scripts/deploy-minion.sh                # builds linux/amd64 from minion/, pushes :latest

# 3. Create the rest of the stack (Job, Scheduler, SAs, IAM, kill-switch)
terraform -chdir=infra apply \
  -var="billing_account=XXXXXX-XXXXXX-XXXXXX"   # your billing account id

# 4. Bump the Job to the freshly-built image (now that the Job exists)
./scripts/deploy-minion.sh

# 5. Manual smoke — run the pipeline once, end to end
gcloud run jobs execute minion --region=europe-west1 --wait
```

**Verify the smoke** in the repo, not in a console — the commit *is* the publication:

```bash
git -C . fetch && git -C . log --oneline origin/main -3
```

Expect a `feat: add YYYY-MM-DD article` commit touching
`site/src/content/articles/{date}.md`, `site/public/images/{date}.png` and `linkedin/{date}.md`,
and the Pages workflow running off it. The run's own trace is in Cloud Logging, filtered on
`run_id`:

```bash
gcloud logging read 'resource.type="cloud_run_job" AND jsonPayload.run_id!=""' \
  --limit=50 --format='value(jsonPayload.message,jsonPayload.step,jsonPayload.status)'
```

**Confirm the daily trigger:** the Scheduler job `minion-daily` (cron `0 6 * * *` Europe/Paris) is
created enabled by Terraform. Force one to validate the trigger path end to end:

```bash
gcloud scheduler jobs run minion-daily --location=europe-west1
```

Then confirm the first real **06:00** run lands the next morning.

## 2. Routine deploy (new image)

```bash
./scripts/deploy-minion.sh                # build + push + bump the Job image
gcloud run jobs execute minion --region=europe-west1 --wait   # optional smoke
```

## 3. OAuth re-auth (Gmail / Anthropic)

Two OAuth credentials can revoke out from under a production run. A run that hard-fails on auth
surfaces a `gmail: …` or `generate: …` error in the run's final log line. Each procedure below is
self-contained — follow it without prior
context. The Job reads the **latest** secret version on its next run; **no redeploy is needed** after
adding a version.

> **Account precondition applies** (see top of this file): every `gcloud` call needs the personal
> `aurelien.allienne@gmail.com` account on project `veilleur-app`. Append
> `--account=aurelien.allienne@gmail.com --project=veilleur-app` to be safe.

### 3a. Gmail OAuth refresh-token revoked (`gmail-oauth-refresh-token`)

Symptom: the run fails at the `gmail` step, error contains `invalid_grant` / `Token has been
expired or revoked`. Google revokes refresh tokens on password change, scope change, 6-month
inactivity, or manual revocation at <https://myaccount.google.com/permissions>.

You re-consent locally to mint a fresh `authorized_user.json`, then push it as a new secret version.
This reuses the **same OAuth client** seeded for the spike (`gmail.readonly` scope, Desktop app).

```bash
# 1. Re-run the local consent flow against the existing OAuth client JSON (the Desktop-app
#    client downloaded from console.cloud.google.com/apis/credentials). A browser opens; sign
#    in as the operator and approve gmail.readonly. The fresh refresh token prints as JSON.
uv --project minion run python -c "
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file(
    'PATH/TO/DOWNLOADED_CLIENT.json',
    ['https://www.googleapis.com/auth/gmail.readonly'])
creds = flow.run_local_server(port=0)
print(creds.to_json())
" > authorized_user.json

# 2. Sanity-check the blob has refresh_token / client_id / client_secret (token_uri optional).
cat authorized_user.json    # must NOT contain a transient access token only

# 3. Push it as a new secret version (Job picks it up next run; no redeploy).
gcloud secrets versions add gmail-oauth-refresh-token --data-file=authorized_user.json \
  --account=aurelien.allienne@gmail.com --project=veilleur-app

# 4. Clean up the local secret material.
rm authorized_user.json
```

If you no longer have the OAuth **client** JSON, re-create the Desktop-app client first — see the
`gmail-oauth-refresh-token` block printed by `scripts/add-secret-versions.sh` (step 1 there). Then
verify with a manual replay: `gcloud run jobs execute minion --region=europe-west1 --wait`.

### 3b. Anthropic / Claude Code OAuth expired (`anthropic-oauth-token`)

Symptom: the run fails at the `generate` step on an auth/401 error. The Claude Code OAuth token is
valid ~1 year, so this is rare — but rotation or manual revocation triggers it.

```bash
# 1. Mint a fresh token (opens a browser; sign in to the Anthropic account). Prints one line
#    starting "sk-ant-oat-...". Do NOT wrap it in quotes.
claude setup-token

# 2. Push it as a new secret version. printf (no trailing newline) keeps the value byte-exact.
printf %s 'sk-ant-oat-PASTE_HERE' | gcloud secrets versions add anthropic-oauth-token \
  --data-file=- --account=aurelien.allienne@gmail.com --project=veilleur-app
```

The `generate` subprocess injects this as `CLAUDE_CODE_OAUTH_TOKEN`
(`minion/src/minion/generate/runner.py`). Verify with a manual replay as above.

### 3c. API-key fallback — break-glass only

The pipeline also works with a raw `ANTHROPIC_API_KEY`, but this is **not a runtime toggle**:
`ANTHROPIC_API_KEY` is deliberately absent from the runtime env, `secrets.py` raises if it is set,
and the runners strip it from the subprocess env. Using it is a deliberate, reviewed code
exception:

1. Create an `anthropic-api-key` secret and grant `minion-sa` accessor on it.
2. In a short-lived PR, change `_build_env()` in `minion/src/minion/generate/runner.py` (and its
   siblings in `fiches/runner.py` and `publish/imagen.py`) to inject `ANTHROPIC_API_KEY` from that
   secret **instead of** `CLAUDE_CODE_OAUTH_TOKEN`, and relax the guard in
   `minion/src/minion/secrets.py`. Say why in the PR body.
3. Deploy, run, and **revert the exception** once OAuth is restored.

Prefer 3b whenever possible. Note the cost consequence: OAuth via the Max plan is metered against
the subscription, an API key is billed per token and will move the monthly budget.

## 4. Budget kill-switch operation

- **What it does:** at 100% of the `budget_amount_eur` cap, the billing budget publishes
  to the `budget-killswitch` Pub/Sub topic; the `budget-killswitch` Cloud Function **pauses** the
  `minion-daily` Scheduler job. No further automated runs fire.
- **Re-enable after a trip (manual, deliberate):**
  ```bash
  gcloud scheduler jobs resume minion-daily --location=europe-west1
  ```
- **Disabling the kill-switch itself should go through a PR** — never remove `infra/killswitch.tf`
  or detach the budget out-of-band. It is the only thing standing between a runaway loop and the
  bill.

## 5. Recovery — replay a missed or failed day

Runs are idempotent by date, and replaying overwrites cleanly: the commit paths are keyed by date,
and the Gmail window is a pure function of the date (the 24h ending at 06:00 Paris), so a replay
sees exactly the same mailbox slice as the original run.

```bash
gcloud run jobs execute minion --region=europe-west1 \
  --args="run,--date,YYYY-MM-DD" --wait
```

A replay re-generates from scratch, which costs another `/generate` call: nothing is persisted
between the generation and the commit. That is the deliberate trade for having no datastore — the
recovery path is cheap to operate and the artefact, once committed, lives in git forever.

You can also run the whole pipeline locally with the four secrets in the environment, which is
faster to iterate on than a Job execution:

```bash
uv --project minion run python -m minion run --date YYYY-MM-DD
```
