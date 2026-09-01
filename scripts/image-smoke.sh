#!/usr/bin/env bash
# scripts/image-smoke.sh
#
# In-image smoke test for the Minion image: asserts the agentic toolchain and the vendored
# `/generate` command are present, and that the CLI entrypoint resolves.
#   docker buildx build --platform linux/amd64 -t le-veilleur-minion:dev --load minion/
#   ./scripts/image-smoke.sh le-veilleur-minion:dev
#
# Exits non-zero on the first failed check.

set -euo pipefail

IMAGE="${1:?usage: image-smoke.sh <image>}"

# Override the entrypoint so we can run individual checks as the (non-root) image user.
# Use a NON-login shell (`-c`, not `-lc`): a login shell sources /etc/profile and resets PATH,
# which would shadow the venv's python at /opt/venv/bin with the base-image python.
run() { docker run --rm --entrypoint bash "$IMAGE" -c "$1"; }

echo ">> git present"
run "command -v git >/dev/null && git --version"

echo ">> node present"
run "command -v node >/dev/null && node --version"

echo ">> claude CLI present"
run "command -v claude >/dev/null && claude --version"

echo ">> /generate command vendored"
run "test -f \"\$HOME/.claude/commands/generate.md\" && head -1 \"\$HOME/.claude/commands/generate.md\""

echo ">> minion CLI resolves"
run "python -m minion --help >/dev/null && echo 'minion --help ok'"

echo ">> running as non-root"
run "test \"\$(id -u)\" != '0' && echo \"uid=\$(id -u) ($(whoami 2>/dev/null || echo minion))\""

echo "SMOKE OK: $IMAGE"
