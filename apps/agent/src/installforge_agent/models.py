"""Domain models for InstallForge, mirroring packages/schemas/*.json.

These Pydantic models are the runtime contract for recipes and device snapshots.
`extra="forbid"` keeps recipes honest: unknown keys fail validation.
"""
from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

OsName = Literal["macos", "linux", "windows", "ios", "android"]
Arch = Literal["arm64", "x86_64", "universal", "any"]
Confidence = Literal["low", "medium", "high"]
Constraint = Literal["no-sudo", "offline", "metered-network", "corporate-proxy", "ci"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Platform(_Strict):
    os: OsName
    arch: Arch
    os_version: Optional[str] = None


class Check(_Strict):
    run: str
    description: Optional[str] = None
    shell: Optional[str] = None
    expect_exit_code: int = 0
    expect_stdout_contains: Optional[str] = None
    expect_stdout_regex: Optional[str] = None


class Step(_Strict):
    id: str
    description: str
    run: str
    shell: Optional[str] = None
    expect: Optional[Check] = None
    timeout_seconds: Optional[int] = None
    elevated: bool = False
    idempotent: bool = True


class Prerequisite(_Strict):
    id: str
    description: str
    check: str
    install_recipe: Optional[str] = None
    required: bool = True


class Detect(_Strict):
    stdout_regex: Optional[str] = None
    stderr_regex: Optional[str] = None
    exit_code: Optional[int] = None


class KnownIssue(_Strict):
    id: str
    symptom: str
    detect: Detect
    cause: str
    fix: List[Step]
    source: Optional[str] = None
    confidence: Optional[Confidence] = None


class Target(_Strict):
    platform: Platform
    steps: List[Step]
    verify: List[Check]
    prerequisites: List[Prerequisite] = Field(default_factory=list)
    known_issues: List[KnownIssue] = Field(default_factory=list)


class Recipe(_Strict):
    id: str
    product: str
    description: str
    recipe_version: str
    targets: List[Target]
    homepage: Optional[str] = None
    source_docs: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    maintainers: List[str] = Field(default_factory=list)
    last_tested: Optional[str] = None

    def target_for(self, os: str, arch: str) -> Optional[Target]:
        """Return the best target for an (os, arch), honoring 'any'/'universal' arch."""
        for target in self.targets:
            if target.platform.os != os:
                continue
            if target.platform.arch in (arch, "any", "universal"):
                return target
        return None


class DeviceConfig(_Strict):
    os: OsName
    arch: Arch
    os_version: Optional[str] = None
    package_managers: List[str] = Field(default_factory=list)
    shell: Optional[str] = None
    installed: Dict[str, str] = Field(default_factory=dict)
    constraints: List[Constraint] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)


class StepResult(_Strict):
    step_id: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    ok: bool = False
    applied_fix: Optional[str] = None


class RunReport(_Strict):
    recipe_id: str
    device: DeviceConfig
    succeeded: bool
    steps: List[StepResult] = Field(default_factory=list)
    verified: bool = False
    notes: List[str] = Field(default_factory=list)
