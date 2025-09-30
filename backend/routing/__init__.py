from .percentage_router import percentage_router
from .ip_router import ip_router
from .header_router import header_router
from .cookie_router import cookie_router

ROUTERS = {
    "percentage": percentage_router,
    "ip": ip_router,
    "header": header_router,
    "cookie": cookie_router
}

def decide_version(request, config):
    """
    Evaluate routers in order specified by config['rulesOrder'].
    Each router returns 'blue'|'green' or None.
    """
    order = config.get("rulesOrder", ["header", "cookie", "ip", "percentage"])
    for rule in order:
        router = ROUTERS.get(rule)
        if router is None:
            continue
        try:
            v = router(request, config)
            if v in ("blue", "green"):
                return v
        except Exception:
            # fail-safe: continue chain
            continue
    # fallback
    return "blue"

