"""Credential resolution helpers for stable local test execution."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


def get_credential(variable_name: str) -> str | None:
    """
    Resolve credentials from multiple sources in priority order.

    Order:
    1) Current process environment.
    2) Windows user environment (values saved using `setx`).
    3) Local `.env` file in project root.
    """
    value = os.getenv(variable_name)
    if value:
        return value

    value = _read_windows_user_env(variable_name)
    if value:
        os.environ[variable_name] = value
        return value

    value = _read_from_dotenv(variable_name)
    if value:
        os.environ[variable_name] = value
        return value

    return None


def bootstrap_credentials(variable_names: tuple[str, ...] = ("SF_USERNAME", "SF_PASSWORD")) -> None:
    """Best-effort preload to reduce missing-env startup failures."""
    for name in variable_names:
        get_credential(name)


def _read_windows_user_env(variable_name: str) -> str | None:
    """Read persisted user environment value from Windows registry."""
    if os.name != "nt":
        return None

    try:
        result = subprocess.run(
            ["reg", "query", r"HKCU\Environment", "/v", variable_name],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None

    if result.returncode != 0 or not result.stdout:
        return None

    for line in result.stdout.splitlines():
        if variable_name not in line:
            continue
        match = re.search(rf"{re.escape(variable_name)}\s+REG_\w+\s+(.*)$", line)
        if match:
            value = match.group(1).strip()
            return value or None
    return None


def _read_from_dotenv(variable_name: str) -> str | None:
    """Read credential from local .env file if present."""
    dotenv_path = Path(__file__).resolve().parent / ".env"
    if not dotenv_path.exists():
        return None

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() != variable_name:
            continue
        cleaned = value.strip().strip('"').strip("'")
        return cleaned or None
    return None
