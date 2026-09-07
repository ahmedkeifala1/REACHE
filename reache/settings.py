"""Django settings for the REACHE Last-Mile website."""

import os
from pathlib import Path

import dj_database_url

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
    "django_ckeditor_5",
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

# The site runs on PostgreSQL. DATABASE_URL chooses the server; the default is
# the local one the README's "Getting started" section sets up.
#
# Vercel cannot reach a PostgreSQL running on a laptop, so a deployment that has
# no DATABASE_URL of its own falls back to the read-only SQLite copy bundled with
# it -- writes there are lost at the next cold start (see "The database is
# ephemeral" in the README). Setting DATABASE_URL on the Vercel project to a
# hosted PostgreSQL is the single change that makes the live admin durable.
LOCAL_DATABASE_URL = "postgres://postgres@127.0.0.1:5432/reache"
DATABASE_URL = os.environ.get("DATABASE_URL", "" if ON_VERCEL else LOCAL_DATABASE_URL)

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            # Serverless instances are created and destroyed constantly, and each
            # one holding a connection open between invocations would exhaust the
            # server's connection slots. Locally, reusing them is the faster choice.
            conn_max_age=0 if ON_VERCEL else 600,
            conn_health_checks=not ON_VERCEL,
        )
    }
else:
    import shutil

    _bundled_db = BASE_DIR / "db.sqlite3"
    _runtime_db = Path("/tmp/db.sqlite3")
    _runtime_db.parent.mkdir(parents=True, exist_ok=True)
    if _bundled_db.exists() and not _runtime_db.exists():
        shutil.copyfile(_bundled_db, _runtime_db)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": _runtime_db,
        }
    }

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

# --- Rich text editing ------------------------------------------------------
# The body fields are HTML, so editors get CKEditor 5 rather than a textarea of
# raw markup. "default" is deliberately the only configuration: every rich field
# on the site offers the same toolbar, so there is nothing for an editor to
# relearn moving between a page, a post and a programme.
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|",
            "bold", "italic", "underline", "link", "|",
            "bulletedList", "numberedList", "blockQuote", "|",
            "insertImage", "insertTable", "mediaEmbed", "|",
            "outdent", "indent", "|",
            "removeFormat", "sourceEditing", "undo", "redo",
        ],
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Heading", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Subheading", "class": "ck-heading_heading3"},
            ],
        },
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:alignLeft", "imageStyle:full", "imageStyle:alignRight",
            ],
            "styles": ["full", "alignLeft", "alignRight"],
        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"],
        },
        # Without this the editor is about six lines tall and long pages are
        # painful to work in.
        "height": "480px",
        "width": "100%",
    },
}

# Pictures dropped into a rich text field land in media/uploads/ rather than the
# top of MEDIA_ROOT, so editor uploads stay separate from the model ImageFields
# that seed_images manages.
CKEDITOR_5_FILE_STORAGE = "core.storage.EditorUploadStorage"

# Uploading is a staff-only action; the endpoint is otherwise an open file drop.
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "png", "gif", "webp"]
