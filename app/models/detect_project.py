from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Technology:
    category: str
    name: str
    version: str | None = None
    confidence: float = 1.0


@dataclass
class DetectedProject:
    root_path: Path
    name: str
    is_valid_project: bool = False

    languages: list[Technology] = field(default_factory=list)
    frameworks: list[Technology] = field(default_factory=list)
    build_tools: list[Technology] = field(default_factory=list)
    capabilities: list[Technology] = field(default_factory=list)
    providers: list[Technology] = field(default_factory=list)

    detected_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)