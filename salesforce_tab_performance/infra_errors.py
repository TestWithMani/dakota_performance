"""Detect WebDriver/browser infrastructure failures vs tab SLA failures."""

from __future__ import annotations

from typing import Iterator

INFRA_SKIP_PREFIX = "INFRA_SKIP:"

_INFRA_EXCEPTION_NAMES = frozenset(
    {
        "TimeoutError",
        "ReadTimeoutError",
        "ConnectionError",
        "ConnectionResetError",
        "BrokenPipeError",
        "WebDriverException",
        "SessionNotCreatedException",
        "InvalidSessionIdException",
        "NoSuchWindowException",
    }
)

_INFRA_MESSAGE_FRAGMENTS = (
    "Read timed out",
    "ReadTimeoutError",
    "HTTPConnectionPool(host='localhost'",
    'HTTPConnectionPool(host="localhost"',
    "disconnected: not connected to DevTools",
    "chrome not reachable",
    "ERR_CONNECTION_RESET",
    "timed out receiving message from renderer",
)


def iter_exception_chain(exc: BaseException | None) -> Iterator[BaseException]:
    """Walk __cause__ / __context__ without cycles."""
    seen: set[int] = set()
    current = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = current.__cause__ or current.__context__


def is_infrastructure_error(exc: BaseException | None) -> bool:
    """Return True when failure is driver/session connectivity, not tab SLA."""
    if exc is None:
        return False

    for err in iter_exception_chain(exc):
        if type(err).__name__ in _INFRA_EXCEPTION_NAMES:
            return True

        module = getattr(type(err), "__module__", "") or ""
        if module.startswith(("urllib3", "selenium.common.exceptions", "selenium.webdriver")):
            return True

        message = str(err)
        if any(fragment in message for fragment in _INFRA_MESSAGE_FRAGMENTS):
            return True

    return False


def infrastructure_error_summary(exc: BaseException | None) -> str:
    """Short human-readable summary for reports."""
    if exc is None:
        return "unknown infrastructure error"

    chain = list(iter_exception_chain(exc))
    root = chain[-1] if chain else exc
    return f"{type(root).__name__}: {root}"
