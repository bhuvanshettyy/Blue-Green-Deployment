def cookie_router(request, config):
    """
    If the cookie exists and equals 'blue'/'green' return it.
    """
    cookie_name = config.get("cookieName", "pricing_version")
    cookies = request.cookies or {}
    v = cookies.get(cookie_name)
    if not v:
        return None
    v = v.strip().lower()
    if v in ("blue", "green"):
        return v
    return None
