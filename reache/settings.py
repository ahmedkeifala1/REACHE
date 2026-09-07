"""Django settings for the REACHE Last-Mile website."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# The defaults below are development defaults. In production set DJANGO_SECRET_KEY,
# DJANGO_DEBUG=0 and DJANGO_ALLOWED_HOSTS in the environment.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-change-me-in-production-9f2a4c7e1b8d6"
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") not in ("0", "false", "False")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
    if host.strip()
]

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
        if origin.strip()
    ]

# Vercel terminates TLS at the edge and forwards plain HTTP to the function, so
# Django only sees https:// through this header. Without it SECURE_SSL_REDIRECT
# above redirects to itself for ever.
ON_VERCEL = bool(os.environ.get("VERCEL"))
if ON_VERCEL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Serves everything in STATIC_ROOT; there is no separate web server in front
    # of the application on Vercel.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "reache.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "reache.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Everything outside /tmp is read-only on Vercel, so the database that ships with
# the deployment is copied there on cold start. Reads are served from the copy and
# writes succeed, but they live only as long as that instance -- an admin edit or a
# newsletter signup is gone at the next cold start. See "Hosting" in the README for
# the managed-Postgres setup that makes writes durable.
if ON_VERCEL:
    import shutil

    _bundled_db = BASE_DIR / "db.sqlite3"
    _runtime_db = Path("/tmp/db.sqlite3")
    _runtime_db.parent.mkdir(parents=True, exist_ok=True)
    if _bundled_db.exists() and not _runtime_db.exists():
        shutil.copyfile(_bundled_db, _runtime_db)
    DATABASES["default"]["NAME"] = _runtime_db

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
