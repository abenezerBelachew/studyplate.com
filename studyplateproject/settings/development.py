from .base import *



# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # new


# For Django Debug Toolbar
# INTERNAL_IPS = [
#     # ...
#     '127.0.0.1',
#     # ...
# ]

# DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False,}


# TODO: THINGS TO CHANGE:
# Password reset page and text
# Password registration

