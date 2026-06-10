from pathlib import Path

from app.models.detect_project import DetectedProject
from app.validation.project_detector import ProjectDetector


class OpenProjectWorkflow:
    """Coordena a abertura e detecção de um projeto."""

    def __init__(
        self,
        detector: ProjectDetector | None = None,
    ) -> None:
        self.detector = detector or ProjectDetector()

    def execute(
        self,
        project_path: str | Path,
    ) -> DetectedProject:
        return self.detector.detect(project_path)