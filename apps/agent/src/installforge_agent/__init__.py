"""InstallForge skill-agent package.

Kept import-light on purpose: importing this package must not pull in heavy or
optional dependencies (typer, httpx). Submodules import what they need.
"""
from __future__ import annotations

__version__ = "0.0.1"
