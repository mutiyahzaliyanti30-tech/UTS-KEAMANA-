from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# PERINGATAN: SECRET_KEY ini hanya untuk keperluan tugas/demo lokal.
# Untuk deployment sungguhan, JANGAN hardcode SECRET_KEY di source code —
# ambil dari environment variable (mis. os.environ["SECRET_KEY"]).
# --------------------------------------------------------------------------
SECRET_KEY = "django-insecure-ganti-key-ini-untuk-produksi-jangan-dipakai-asli"

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "secure_auth_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "secure_auth_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------------------------------
# VALIDASI PASSWORD — menolak password lemah/umum/mirip data user/hanya angka.
# Ini yang membuat "Broken Authentication" jadi lebih sulit dieksploitasi.
# --------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------
# KEAMANAN SESSION & COOKIE
# --------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True          # cookie session tidak bisa diakses lewat JavaScript (mitigasi XSS)
CSRF_COOKIE_HTTPONLY = True             # cookie CSRF token juga tidak bisa dibaca JavaScript
SESSION_COOKIE_SAMESITE = "Lax"         # mitigasi CSRF dari situs pihak ketiga
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # session otomatis habis saat browser ditutup
SESSION_COOKIE_AGE = 30 * 60            # session otomatis expired setelah 30 menit tidak aktif

X_FRAME_OPTIONS = "DENY"                # mitigasi Clickjacking (tidak boleh ditaruh di dalam <iframe>)

# --------------------------------------------------------------------------
# UNTUK PRODUKSI (di server sungguhan dengan HTTPS aktif), aktifkan baris di
# bawah ini. Dimatikan di sini karena runserver lokal masih pakai HTTP biasa.
# --------------------------------------------------------------------------
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# --------------------------------------------------------------------------
# PENGATURAN LOCKOUT LOGIN (dipakai manual di accounts/views.py)
# --------------------------------------------------------------------------
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15
