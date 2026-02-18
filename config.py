import os
from pathlib import Path

# Base data directory
DATA_DIR = Path(os.path.expanduser("~/.local/share/sideshelf"))
DB_PATH = DATA_DIR / "sideshelf.db"
IMAGE_DIR = DATA_DIR / "images"

# TTL for clipboard items (7 days in seconds)
TTL_SECONDS = 7 * 24 * 60 * 60

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
