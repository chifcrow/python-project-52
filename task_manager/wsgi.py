"""
WSGI config for task_manager project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

application = get_wsgi_application()

# Rollbar initialization (production only).
ROLLBAR_ACCESS_TOKEN = os.getenv("ROLLBAR_ACCESS_TOKEN", "").strip()
ROLLBAR_ENV = os.getenv("ROLLBAR_ENV", "development").strip()
DEBUG = os.getenv("DEBUG", "true").lower() in {"1", "true", "yes", "on"}
ROLLBAR_ENABLED = os.getenv("ROLLBAR_ENABLED", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

if not DEBUG and ROLLBAR_ENABLED and ROLLBAR_ACCESS_TOKEN:
    import rollbar

    rollbar.init(
        access_token=ROLLBAR_ACCESS_TOKEN,
        environment=ROLLBAR_ENV,
        root=os.path.dirname(os.path.dirname(__file__)),
        allow_logging_basic_config=False,
    )
