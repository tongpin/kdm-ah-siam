import os
import yaml
CONFIG_PATH = os.getenv("CONFIG_PATH", "config.yml")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    raw = yaml.safe_load(f)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or raw["telegram"]["token"]
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", ",".join(map(str, raw["telegram"]["admin_ids"]))).split(",") if x.strip()]
WEB_HOST = os.getenv("WEB_HOST", raw["web"]["host"])
WEB_PORT = int(os.getenv("SERVER_PORT", os.getenv("PORT", raw["web"]["port"])))
DATA_FILE = os.getenv("DATA_FILE", raw["app"]["data_file"])
MINI_APP_URL = os.getenv("MINI_APP_URL", raw["app"]["mini_app_url"])
