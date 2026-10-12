import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
load_dotenv(BASE_DIR.parent / '.env')

DEFAULT_DB_URL = (
    'postgresql://jewellery_admin:ft7OhmzQkI41l8hpPhwXRnI1IHDRsYVu'
    '@dpg-db3ppo8473hc73etsch0-a.oregon-postgres.render.com/jewellery_shop_nuns'
)

database_url = os.environ.get('DATABASE_URL', DEFAULT_DB_URL)
# Fix Render's legacy 'postgres://' scheme to 'postgresql://' for SQLAlchemy 1.4+
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cafe-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
