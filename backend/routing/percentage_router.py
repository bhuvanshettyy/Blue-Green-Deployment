import hashlib
import time

def _seed_for_request(request, config):
    # Prefer existing cookie (so deterministic for a client). Fallback to X-Request-Id header, then IP, then timestamp
    cookie_name = config.get("cookieName", "pricing_version")
    cookies = request.cookies or {}
    if cookies.get(cookie_name):
        return cookies.get(cookie_name)
    rid = request.headers.get("x-request-id")
    if rid:
        return rid
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    client = getattr(request, "client", None)
    if client:
        return client.host
    # last fallback: time-based deterministic-ish but not sticky
    return str(int(time.time() * 1000))

def percentage_router(request, config):
    weights = config.get("percentage", {"blue": 50, "green": 50})
    blue = int(weights.get("blue", 50))
    green = int(weights.get("green", 50))
    total = blue + green
    if total <= 0:
        return "blue"
    seed = _seed_for_request(request, config)
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    num = int(h[:8], 16)
    bucket = num % total
    return "blue" if bucket < blue else "green"
