"""
Django settings for the «Альошин та Партнери» promo site.

Конфіг навмисно мінімальний: сайт статичний, бази даних немає.
Сторінки рендеряться як шаблони, картинки з assets/ віддаються через WhiteNoise.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


# --- Безпека ------------------------------------------------------------
# На хостингу обовʼязково встанови змінну оточення DJANGO_SECRET_KEY.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "insecure-dev-key-change-me-on-production",
)

DEBUG = env_bool("DJANGO_DEBUG", default=False)

# Кома-розділений список доменів, напр.: "aleshin.com.ua,www.aleshin.com.ua"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")
    if h.strip()
]

# Якщо вкажеш домени — додаємо їх до CSRF trusted origins (https).
CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if h not in ("*", "localhost", "127.0.0.1")
]


# --- Застосунки ---------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise віддає статику без окремого веб-сервера.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- Статика ------------------------------------------------------------
# Віддаємо assets/ за тим самим шляхом /assets/..., що й у HTML,
# тому правити верстку не треба.
STATIC_URL = "/assets/"
STATICFILES_DIRS = [BASE_DIR / "assets"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# --- Локалізація --------------------------------------------------------
LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = False
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- HTTPS за проксі (cPanel/Passenger) ---------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
