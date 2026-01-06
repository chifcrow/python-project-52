#!/usr/bin/env bash
set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"


PY_CANDIDATE="$(ls -1 /opt/render/project/python/Python-*/bin/python3 2>/dev/null \
  | head -n 1 || true)"

if [[ -n "${PY_CANDIDATE}" ]]; then
  export UV_PYTHON="${PY_CANDIDATE}"
  export PATH="$(dirname "${PY_CANDIDATE}"):${PATH}"
else
  export UV_PYTHON="python3.10"
fi

make install
make collectstatic
make migrate
