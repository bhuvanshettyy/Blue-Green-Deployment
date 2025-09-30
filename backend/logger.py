import json
import os
from datetime import datetime


LOG_PATH = os.path.join(os.path.dirname(__file__), "requests.log")

def log_request(meta: dict):
    meta_line = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        **meta
    }
    line = json.dumps(meta_line)
    # write to stdout and file
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


