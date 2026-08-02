from fastapi import Request

from app.core.logging import logger


def _add_usage(request: Request, usage: dict) -> None:

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


def accumulate_usage(request: Request, message) -> None:
    """
    Adds an LLM response message's token usage onto
    request.state.token_usage, so TokenUsageMiddleware (or
    log_token_usage, for streaming endpoints) can log the running
    total once the request finishes. A single request can involve
    more than one LLM call (the assistant's tool-calling loop can call
    the model several times), so this adds to whatever is already
    there instead of overwriting it.

    Use this when you have the AIMessage/AIMessageChunk itself, e.g.
    from a plain or streaming chat model call.
    """

    _add_usage(request, getattr(message, "usage_metadata", None))


def accumulate_usage_from_callback(request: Request, callback) -> None:
    """
    Same as accumulate_usage(), but reads from a
    langchain_core.callbacks.usage.UsageMetadataCallbackHandler
    instead of a message.

    Use this around with_structured_output(...) chains: those can
    return just the parsed schema object with no usage_metadata
    attached, and forcing include_raw=True to get the raw message
    changes parse failures from a raised exception into a returned
    value, which silently defeats .with_retry() (see
    chains/extract_lead.py). The callback observes the raw model
    response directly, so it works regardless of how the chain's
    output parser handles - or fails to handle - the result.
    """

    for usage in callback.usage_metadata.values():
        _add_usage(request, usage)


def log_token_usage(request: Request, elapsed_ms: float = None) -> None:
    """
    Logs whatever usage accumulate_usage()/accumulate_usage_from_callback()
    has collected on this request, if any.

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
