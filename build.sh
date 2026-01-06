#!/usr/bin/env bash
set -euo pipefail

# Install uv (Render build environment)
curl -LsSf https://astral.sh/uv/install.sh | sh
# shellcheck disable=SC1091
source "$HOME/.local/bin/env"

# Ensure uv uses a real Python interpreter (Render may prepend wrapper scripts)
export UV_PYTHON="python3.10"

make install
make collectstatic
make migrate
