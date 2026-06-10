"""Device probing: build a DeviceConfig snapshot of the current machine."""
from __future__ import annotations

import platform
import shutil
from typing import List

from .models import Arch, DeviceConfig, OsName

_KNOWN_PACKAGE_MANAGERS = [
    "brew",
    "apt-get",
    "dnf",
    "pacman",
    "zypper",
    "snap",
    "flatpak",
    "choco",
    "winget",
]


def _detect_os() -> OsName:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    return "linux"


def _detect_arch() -> Arch:
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "arm64"
    if machine in ("x86_64", "amd64"):
        return "x86_64"
    return "any"


def detect_package_managers() -> List[str]:
    return [pm for pm in _KNOWN_PACKAGE_MANAGERS if shutil.which(pm)]


def probe_device() -> DeviceConfig:
    """Best-effort snapshot of the current device.

    TODO: enrich `installed` with versions of common tools, and detect constraints
    (no-sudo, offline, corporate-proxy). See docs/spec.md "Device probing".
    """
    return DeviceConfig(
        os=_detect_os(),
        arch=_detect_arch(),
        os_version=platform.release(),
        package_managers=detect_package_managers(),
    )
