from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    app_name = "PocketSmart AI"
    secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'pocketsmart.db'}")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    upload_dir = BASE_DIR / os.getenv("UPLOAD_DIR", "app/static/uploads")
    max_upload_mb = int(os.getenv("MAX_UPLOAD_MB", "5"))
    demo_mode = os.getenv("DEMO_MODE", "true").lower() in {"1", "true", "yes", "on"}

settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
