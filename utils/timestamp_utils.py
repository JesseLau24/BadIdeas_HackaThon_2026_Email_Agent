import json
import os
from datetime import datetime, timedelta, timezone
from utils.constants import LAST_PROCESSED_JSON_PATH  # ✅ 新增导入路径常量

# 默认路径改为 data/last_processed.json
TIMESTAMP_FILE = LAST_PROCESSED_JSON_PATH

def read_last_processed_timestamp(filename: str = TIMESTAMP_FILE) -> datetime:
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return datetime.fromisoformat(data.get("last_processed")).astimezone(timezone.utc)
    else:
        # Default to 3 days ago if file doesn't exist
        return (datetime.now(timezone.utc) - timedelta(days=3))


def write_last_processed_timestamp(timestamp: datetime, filename: str = TIMESTAMP_FILE):
    # Ensure timestamp is stored as UTC ISO string
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"last_processed": timestamp.astimezone(timezone.utc).isoformat()}, f)
