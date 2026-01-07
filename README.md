### Hexlet tests and linter status:

[![Actions Status](https://github.com/chifcrow/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/chifcrow/python-project-52/actions)

[![Actions Status](https://github.com/chifcrow/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/chifcrow/python-project-52/actions)

# Task Manager

Django-based web application deployed on Render (PaaS).

The project is configured according to modern production practices:

- Python 3.10+
- Django
- PostgreSQL
- uv for dependency management
- Gunicorn as WSGI server
- Environment-based configuration (12-factor app)

---

## Demo

The deployed application is available at:

https://task-manager-a935.onrender.com

Health check endpoint:

https://task-manager-a935.onrender.com/healthz

---

## Tech Stack

- Python 3.10+
- Django
- PostgreSQL
- Gunicorn
- uv
- Render (PaaS)

---

## Local Development

### Requirements

- Python 3.10+
- uv

### Setup

```text
uv sync
```

## Run migrations

```bash
uv run python manage.py migrate
```

## Run development server

```bash
uv run python manage.py runserver
```

## Run development server

```bash
uv run python manage.py runserver
```

Application will be available at:

```bash
http://127.0.0.1:8000
```

## Deployment

The project is deployed on Render using:

- build.sh for build steps
- Makefile for unified commands
- Environment variables for secrets and configuration

Build command on Render:

```bash
make build
```

Start command on Render:

```bash
make render-start
```

## Health Check

Render health checks are handled by the /healthz endpoint, which returns:

```text
ok
```

## Notes

- Secrets are not stored in the repository.
- Database configuration is provided via DATABASE_URL.
- The project follows the Twelve-Factor App methodology.

## License

MIT License

---
