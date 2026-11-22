"""
Django settings for the «Альошин, Хижняк та Партнери» site.

Сторінки рендеряться як шаблони, картинки з assets/ віддаються через WhiteNoise.
Заявки з форм зберігаються в SQLite (застосунок leads), облік — в адмінці /crm/.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Локальний файл .env (не потрапляє в git): KEY=VALUE по рядку.
# Справжні змінні оточення мають перевагу.
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    for _line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _value = _line.split("=", 1)
            os.environ.setdefault(_key.strip(), _value.strip().strip("'\""))


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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "leads",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise віддає статику без окремого веб-сервера.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Canonical, Open Graph і Schema.org з адресою сайту з SITE_URL.
    "config.seo.SeoHeadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- База даних заявок ---------------------------------------------------
# Файл лежить поза статикою й не потрапляє в git. На хостингу шлях можна
# перевизначити змінною DJANGO_DB_PATH.
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_DB_PATH", str(DATA_DIR / "leads.sqlite3")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60 * 12  # вхід у CRM діє 12 годин


# --- Адреса сайту та сповіщення ------------------------------------------
# Домен зміниться — тут він задається в одному місці (без похилої риски в кінці).
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

# Поки на головній адресі стоїть старий сайт, новий відкривається на /corporate.
# У день запуску: SITE_NEW_AT_ROOT=true — і новий сайт стає головною сторінкою.
NEW_SITE_AT_ROOT = env_bool("SITE_NEW_AT_ROOT", default=False)

# Сповіщення про нову заявку в Telegram. Порожні значення = вимкнено.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
# Текст звернення в Telegram не надсилаємо, доки це явно не ввімкнено.
TELEGRAM_INCLUDE_MESSAGE = env_bool("TELEGRAM_INCLUDE_MESSAGE", default=False)


# --- Статика ------------------------------------------------------------
# Віддаємо assets/ за тим самим шляхом /assets/..., що й у HTML,
# тому правити верстку не треба.
STATIC_URL = "/assets/"
STATICFILES_DIRS = [
    BASE_DIR / "assets",
    ("new-site", BASE_DIR / "new-site"),
]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# --- Локалізація --------------------------------------------------------
LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True  # адмінка заявок українською
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- HTTPS за проксі (cPanel/Passenger) ---------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
