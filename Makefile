.PHONY: install start migrate collectstatic build render-start check

UV_PYTHON ?= python3.10

install:
	uv sync --python $(UV_PYTHON)

start:
	uv run python manage.py runserver 0.0.0.0:8000

migrate:
	uv run python manage.py migrate --noinput

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi:application --bind 0.0.0.0:$${PORT:-8000}

check:
	uv run python manage.py check
