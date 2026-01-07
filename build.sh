#!/usr/bin/env bash
set -euo pipefail

echo "==> build.sh: starting"
echo "==> build.sh: initial PATH=${PATH}"

# Install uv (Render build environment)
curl -LsSf https://astral.sh/uv/install.sh | sh
# shellcheck disable=SC1091
source "$HOME/.local/bin/env"

echo "==> build.sh: uv location: $(command -v uv || true)"
echo "==> build.sh: python3 location before fix: $(command -v python3 || true)"

# Prefer Render-installed CPython over wrapper scripts.
PY_CANDIDATE="$(ls -1 /opt/render/project/python/Python-*/bin/python3 2>/dev/null \
  | head -n 1 || true)"

echo "==> build.sh: PY_CANDIDATE=${PY_CANDIDATE}"

if [[ -n "${PY_CANDIDATE}" ]]; then
  export UV_PYTHON="${PY_CANDIDATE}"
  export PATH="$(dirname "${PY_CANDIDATE}"):${PATH}"
else
  export UV_PYTHON="python3.10"
fi

echo "==> build.sh: UV_PYTHON=${UV_PYTHON}"
echo "==> build.sh: python3 location after fix: $(command -v python3 || true)"
echo "==> build.sh: python version: $(${UV_PYTHON} -V 2>&1 || true)"

make install
make collectstatic
make migrate

echo "==> build.sh: done"
