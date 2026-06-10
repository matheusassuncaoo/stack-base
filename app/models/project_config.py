from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Configuração selecionada para gerar um projeto inicial."""

    name: str
    stack: str
    architecture: str
    database: str
    output_directory: Path
    use_docker: bool = True
    use_tests: bool = True
    use_ci: bool = False

    @property
    def project_path(self) -> Path:
        return self.output_directory / self.name
