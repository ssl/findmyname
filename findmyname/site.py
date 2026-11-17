"""What a site is, and how sites are found."""

import importlib.util
import re
import threading
from dataclasses import dataclass, field, replace
from typing import Callable

import requests

from . import REPO_ROOT

SITES_DIR = REPO_ROOT / "sites"


class RetryableError(Exception):
    """The check gave no certain answer and should be tried again."""


@dataclass(frozen=True)
class Site:
    label: str
    pattern: re.Pattern
    check: Callable[[str, dict], bool]
    defaults: dict = field(default_factory=dict)
    name: str = ""


def site_names():
    """The names of all sites, without importing them."""
    return sorted(p.parent.name for p in SITES_DIR.glob("*/checker.py"))


def load_site(name):
    """Import one site's checker and return its Site."""
    path = SITES_DIR / name / "checker.py"
    spec = importlib.util.spec_from_file_location(f"findmyname_site_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return replace(module.SITE, name=name)


_local = threading.local()


def thread_session():
    """A requests.Session per worker thread, so connections are reused."""
    session = getattr(_local, "session", None)
    if session is None:
        session = requests.Session()
        _local.session = session
    return session
