from .base import *
import json
from django.core.exceptions import ImproperlyConfigured


secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

DEBUG = True

# static
STATIC_ROOT = "/vol/web/static"
MEDIA_ROOT = "/vol/web/media"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": get_secret("DB_HOST"),
        "NAME": get_secret("DB_NAME"),
        "USER": get_secret("DB_USER"),
        "PASSWORD": get_secret("DB_PASSWORD"),
    }
}

from config.log_utils import JSONFormatter, JSONSocketHandler

# Logger
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JSONFormatter,
        },
        "timestamp": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/django.jsonl",
            "formatter": "json",
        },
        "tcp": {
            "class": "config.log_utils.JSONSocketHandler",
            "host": "logstash",
            "port": 5044,
            "formatter": "json",
        },
    },
    "loggers": {
        "console": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django": {
            "handlers": ["tcp"],
            "level": "INFO",
        },
    },
}
