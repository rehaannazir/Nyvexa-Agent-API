import time

from fastapi import Request

from app.utils.usage import log_token_usage


async def token_usage_middleware(request: Request, call_next):

    start = time.perf_counter()

    response = await call_next(request)

    if response.headers.get("content-type", "").startswith("text/event-stream"):
        return response

    elapsed = (time.perf_counter() - start) * 1000
    log_token_usage(request, elapsed)

    return response
