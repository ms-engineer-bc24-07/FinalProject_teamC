import os
from pathlib import Path
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()  # .envファイルを読み込む

# 環境変数が正しく読み込まれているか確認
if not os.getenv("FIREBASE_CREDENTIALS_PATH"):
    raise ValueError("FIREBASE_CREDENTIALS_PATH 環境変数が設定されていません。")
if not os.getenv("POSTGRES_DB"):
    raise ValueError("POSTGRES_DB 環境変数が設定されていません。")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# Firebase認証ファイルのパスを環境変数から取得
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not firebase_credentials_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH が設定されていません。")

firebase_credentials_path = BASE_DIR / firebase_credentials_path

# Firebase Admin SDKの初期化
if len(firebase_admin._apps) == 0:  # _apps を確認して、すでに初期化されていない場合のみ実行
    try:
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
        logging.info("Firebaseの初期化が完了しました。")
    except Exception as e:
        logging.error(f"Firebaseの初期化中にエラーが発生しました: {e}")
else:
    logging.info("Firebaseはすでに初期化されています。")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "connetto_backend.urls"

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

WSGI_APPLICATION = "connetto_backend.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Scoring Weights Configuration
SCORING_WEIGHTS = {
    "性別制限": {"同性": 10, "希望なし": 0},
    "年代制限": {"同年代": 8, "幅広い年代": 5, "希望なし": 0},
    "入社年": {"完全一致": 7, "希望なし": 0},
    "部署希望": {"所属部署内希望": 7, "他部署混在": 3, "希望なし": 0},
    "お店の雰囲気": {"落ち着いたお店": 5, "わいわいできるお店": 3, "希望なし": 0},
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
