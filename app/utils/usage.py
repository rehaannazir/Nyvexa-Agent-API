from fastapi import Request

from app.core.logging import logger


def accumulate_usage(request: Request, message) -> None:
    """
    Adds an LLM response's token usage onto request.state.token_usage,
    so TokenUsageMiddleware can log the running total once the request
    finishes. A single request can involve more than one LLM call (the
    assistant's tool-calling loop can call the model several times), so
    this adds to whatever is already there instead of overwriting it.
    """

    usage = getattr(message, "usage_metadata", None)

    if not usage:
        return

    totals = getattr(request.state, "token_usage", None) or {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }

    totals["prompt_tokens"] += usage.get("input_tokens", 0) or 0
    totals["completion_tokens"] += usage.get("output_tokens", 0) or 0
    totals["total_tokens"] += usage.get("total_tokens", 0) or 0

    request.state.token_usage = totals


def log_token_usage(request: Request, elapsed_ms: float = None) -> None:
    """
    Logs whatever usage accumulate_usage() has collected on this
    request, if any.

    Used by TokenUsageMiddleware for ordinary (non-streaming)
    responses. Streaming endpoints (like the assistant) call this
    directly instead of relying on the middleware - middleware only
    gets control back once the streamed response *starts*, not once
    it *finishes*, so checking request.state there would catch the
    usage only partway accumulated.
    """

    usage = getattr(request.state, "token_usage", None)

    if not usage:
        return

    logger.info(
        "Path=%s Prompt=%s Completion=%s Total=%s Latency=%s",
        request.url.path,
        usage["prompt_tokens"],
        usage["completion_tokens"],
        usage["total_tokens"],
        f"{elapsed_ms:.2f}ms" if elapsed_ms is not None else "n/a",
    )
