import hashlib

def _get_client_ip(request):
    # Try X-Forwarded-For fallback then client.host
    xff = request.headers.get("x-forwarded-for")
    if xff:
        # may contain multiple, take first
        ip = xff.split(",")[0].strip()
        return ip
    # Starlette request.client is a tuple (host, port)
    client = getattr(request, "client", None)
    if client:
        return client.host
    return None

def ip_router(request, config):
    """
    Map IP deterministically to blue/green using hash and percentages.
    Supports optional explicit ipMap in config: { "1.2.3.4": "green" }
    """
    ip = _get_client_ip(request)
    if not ip:
        return None
    ip_map = config.get("ipMap", {})
    if ip in ip_map:
        v = ip_map[ip].lower()
        if v in ("blue", "green"):
            return v

    weights = config.get("percentage", {"blue": 50, "green": 50})
    blue = int(weights.get("blue", 50))
    green = int(weights.get("green", 50))
    total = blue + green
    if total <= 0:
        return "blue"

    h = hashlib.sha256(ip.encode("utf-8")).hexdigest()
    num = int(h[:8], 16)  # 32-bit sample
    bucket = num % total
    return "blue" if bucket < blue else "green"
