"""Passive update checker — hits GitHub releases API, caches daily."""

import json
import os
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError

from typer_cli import __version__

REPO = "William-Ger/typer"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
CACHE_DIR = os.path.expanduser("~/.config/typer")
CACHE_FILE = os.path.join(CACHE_DIR, "update_cache.json")
CHECK_INTERVAL = 86400  # 1 day in seconds


def _read_cache():
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_cache(data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)


def _fetch_latest():
    """Fetch latest release tag from GitHub. Returns version string or None."""
    try:
        req = Request(API_URL, headers={"Accept": "application/vnd.github+json"})
        with urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            tag = data.get("tag_name", "")
            return tag.lstrip("v")
    except (URLError, OSError, json.JSONDecodeError, KeyError):
        return None


def _parse_version(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except (ValueError, AttributeError):
        return (0,)


def _is_newer(latest, current):
    return _parse_version(latest) > _parse_version(current)


def detect_install_method():
    """Detect how typer was installed. Returns 'brew' or 'pip'."""
    exe = sys.executable or ""
    if "/Cellar/" in exe or "/homebrew/" in exe or "/linuxbrew/" in exe:
        return "brew"
    return "pip"


def get_update_info():
    """Check for updates (cached daily).

    Returns dict with:
        version: current version string
        latest: latest version string or None
        update_available: bool
        install_method: 'brew' or 'pip'
        update_cmd: shell command to update
    """
    info = {
        "version": __version__,
        "latest": None,
        "update_available": False,
        "install_method": detect_install_method(),
        "update_cmd": "",
    }

    try:
        cache = _read_cache()
        last_check = cache.get("last_check", 0)
        cached_latest = cache.get("latest_version")

        if time.time() - last_check < CHECK_INTERVAL and cached_latest:
            latest = cached_latest
        else:
            latest = _fetch_latest()
            if latest:
                _write_cache({"last_check": time.time(), "latest_version": latest})

        if latest and _is_newer(latest, __version__):
            info["latest"] = latest
            info["update_available"] = True
    except Exception:
        pass

    if info["install_method"] == "brew":
        info["update_cmd"] = "brew upgrade typer"
    else:
        info["update_cmd"] = "pip install --upgrade typer-cli-tool"

    return info
