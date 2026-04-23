import time
from collections import defaultdict

from fastapi import HTTPException, Request, status
from config.settings import settings

RATE_STORE = defaultdict(list)


def rate_limit(request: Request):
    key = f"{request.client.host}:{request.url.path}"
    window = time.time() - 60
    entries = [ts for ts in RATE_STORE[key] if ts > window]
    if len(entries) >= settings.RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please wait before retrying.",
        )
    entries.append(time.time())
    RATE_STORE[key] = entries
