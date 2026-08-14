"""Centralised configuration — all secrets and tunables in one place.

Values are read from environment variables. A local `.env` file is loaded
automatically at startup if present.
"""

import os

def load_dotenv(dotenv_path=".env"):
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key:
                        os.environ.setdefault(key, val)

# Load environment variables from .env file
load_dotenv()

# ── Telegram Bot ───────────────────────────────────────────────
API_ID = int(os.environ.get("API_ID", 2040))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP = os.environ.get("TG_GROUP", "shona_support")
CHANNEL = os.environ.get("TG_CHANNEL", "shona_bots")

# ── API Base URL ───────────────────────────────────────────────
BASE_URL = os.environ.get("BASE_URL", "https://api.nubcoders.com").rstrip("/")

admin_ids_str = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS = [int(x) for x in admin_ids_str.split() if x.isdigit()]

# ── Redis ──────────────────────────────────────────────────────
# If REDIS_URL is set (e.g. by a Heroku Redis addon: redis://user:pass@host:port
# or rediss://... for TLS), auto-split it into the discrete vars below.
# Explicit REDIS_HOST / REDIS_PORT / REDIS_USERNAME / REDIS_PASSWORD (if set)
# always take priority over REDIS_URL.
_redis_url = os.environ.get("REDIS_URL")
if _redis_url:
    from urllib.parse import urlparse
    _parsed = urlparse(_redis_url)
    REDIS_HOST = os.environ.get("REDIS_HOST", _parsed.hostname or "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", _parsed.port or 15440))
    REDIS_USERNAME = os.environ.get("REDIS_USERNAME", _parsed.username or "default")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", _parsed.password)
    REDIS_SSL = os.environ.get("REDIS_SSL", "1" if _parsed.scheme == "rediss" else "0") == "1"
else:
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 15440))
    REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "default")
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
    REDIS_SSL = os.environ.get("REDIS_SSL", "0") == "1"

# ── Cookies ────────────────────────────────────────────────────
# Path to the Netscape cookies file yt-dlp reads. Bootstrapped once at
# startup from the browser profile (see utils/cookies.py).
COOKIES_FILE = os.environ.get("COOKIES_FILE", "cookies.txt")
COOKIES_BROWSER = os.environ.get("COOKIES_BROWSER", "firefox")
# URL hit once at startup to export browser cookies into COOKIES_FILE.
COOKIES_BOOTSTRAP_URL = os.environ.get(
    "COOKIES_BOOTSTRAP_URL", "https://www.youtube.com/watch?v=BaW_jenozKc"
)
# Re-export cookies from the browser every N hours (0 disables).
COOKIES_REFRESH_HOURS = float(os.environ.get("COOKIES_REFRESH_HOURS", 6))

# ── Rate Limits ────────────────────────────────────────────────
DAILY_LIMIT = int(os.environ.get("DAILY_LIMIT", 1000))
ADMIN_LIMIT = int(os.environ.get("ADMIN_LIMIT", 10000))
