from backend.routing import decide_version
from backend.logger import log_request
import os
import json
from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR.parent / "frontend"


# Load config and allow env overrides
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # overrides
    pct_blue = os.getenv("PCT_BLUE")
    pct_green = os.getenv("PCT_GREEN")
    if pct_blue is not None or pct_green is not None:
        cfg["percentage"] = {
            "blue": int(pct_blue) if pct_blue is not None else cfg.get("percentage", {}).get("blue", 50),
            "green": int(pct_green) if pct_green is not None else cfg.get("percentage", {}).get("green", 50)
        }
    cookie_name = os.getenv("COOKIE_NAME")
    if cookie_name:
        cfg["cookieName"] = cookie_name
    cookie_age = os.getenv("COOKIE_MAX_AGE_DAYS")
    if cookie_age:
        cfg["cookieMaxAgeDays"] = int(cookie_age)
    rules_order = os.getenv("RULES_ORDER")  # e.g., "header,cookie,ip,percentage"
    if rules_order:
        cfg["rulesOrder"] = [r.strip() for r in rules_order.split(",") if r.strip()]
    # ipMap could be extended to parse env if desired
    return cfg

CONFIG = load_config()

app = FastAPI(title="Blue-Green Pricing API")


# CORS (not strictly needed if serving static from same origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # reduce in prod
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

def load_pricing(version: str):
    file_path = DATA_DIR / f"pricing.{version}.json"
    if not file_path.exists():
        return {"name": version, "plans": []}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/pricing")
async def pricing_endpoint(request: Request):
    # Decide version
    chosen = decide_version(request, CONFIG)

    # Sticky cookie: if not set or different, set cookie
    cookie_name = CONFIG.get("cookieName", "pricing_version")
    cookie_max_age_days = CONFIG.get("cookieMaxAgeDays", 30)
    max_age_seconds = int(cookie_max_age_days) * 24 * 60 * 60

    response_payload = {"version": chosen, "pricing": load_pricing(chosen)}
    # Log metadata
    meta = {
        "method": "GET",
        "path": str(request.url.path),
        "client": {
            "host": request.client.host if request.client else None,
            "headers": {
                "user-agent": request.headers.get("user-agent"),
                "x-version": request.headers.get("x-version"),
                "x-forwarded-for": request.headers.get("x-forwarded-for"),
                "x-request-id": request.headers.get("x-request-id")
            }
        },
        "selectedVersion": chosen
    }
    log_request(meta)

    response = JSONResponse(content=response_payload)
    # set cookie if missing or differs
    existing = request.cookies.get(cookie_name)
    if existing != chosen:
        response.set_cookie(key=cookie_name, value=chosen, max_age=max_age_seconds, httponly=True, samesite="lax")
    return response

# Optionally provide a simple healthcheck
@app.get("/health")
async def health():
    return {"status": "ok"}

# Serve frontend static files (mounted last so API routes take precedence)
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
