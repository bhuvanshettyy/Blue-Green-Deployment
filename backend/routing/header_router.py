def header_router(request, config):
    """
    If X-Version header present and valid, honor it.
    Header names not case-sensitive.
    """
    hdr = request.headers.get("x-version")
    if not hdr:
        return None
    v = hdr.strip().lower()
    if v in ("blue", "green"):
        return v
    return None
