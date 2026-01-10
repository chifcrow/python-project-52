#!/usr/bin/env bash

set -euo pipefail

echo "==> build.sh: starting"

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

PY_CANDIDATE="$(ls -1 /opt/render/project/python/Python-*/bin/python3* 2>/dev/null \
  | head -n 1 || true)"

if [[ -n "${PY_CANDIDATE}" ]]; then
  export UV_PYTHON="${PY_CANDIDATE}"
  export PATH="$(dirname "${PY_CANDIDATE}"):${PATH}"
else
  export UV_PYTHON="$(command -v python3)"
fi

echo "==> build.sh: UV_PYTHON=${UV_PYTHON}"
echo "==> build.sh: python version: $(${UV_PYTHON} -V 2>&1 || true)"

make install
make collectstatic
make migrate

echo "==> build.sh: done"
