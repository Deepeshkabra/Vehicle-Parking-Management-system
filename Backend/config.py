import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///parking_app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Set to False in production

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "testing-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # Admin credentials
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
    ADMIN_NAME = os.environ.get("ADMIN_NAME")

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # Your Gmail address
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # App-specific password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com")
    MAIL_DEBUG = True

    BACKEND_URL = "http://localhost:5000"
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    RESULT_BACKEND = "redis://localhost:6379/0"
    CELERY_TIMEZONE = "UTC"
    BEAT_SCHEDULE = {}

    # Celery schedule

    EXPORT_FOLDER = os.environ.get("EXPORT_FOLDER") or './exports'

    # Matplotlib configuration
    MATPLOTLIB_BACKEND = "Agg"

    REPORT_INCLUDE_CHART = True
    MAX_RESERVATIONS_PER_REPORT = 50

    # Redis Caching Configuration
    REDIS_CACHE_URL = 'redis://localhost:6379/1'  # Different DB than Celery
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = 'redis://localhost:6379/1'
    
    # Cache expiry times (in seconds)
    CACHE_EXPIRY = {
        'parking_lots': 600,        # 10 minutes
        'parking_spots': 60,        # 1 minute (changes frequently)
        'user_profile': 1800,       # 30 minutes
        'dashboard_stats': 300,     # 5 minutes
        'user_list': 900,          # 15 minutes
        'session_data': 3600,      # 1 hour
    }



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
