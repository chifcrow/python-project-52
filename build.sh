#!/usr/bin/env bash
set -euo pipefail

# Install uv (Render build environment)
curl -LsSf https://astral.sh/uv/install.sh | sh
# shellcheck disable=SC1091
source "$HOME/.local/bin/env"

# Build steps
make install
make collectstatic
make migrate
