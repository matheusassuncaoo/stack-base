from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SpringMvcAction:
    """Ação planejada para estruturar um projeto Spring Boot no padrão MVC."""

    relative_path: Path
    description: str
    action_type: str
    content: str | None = None


@dataclass
class SpringMvcActionResult:
    """Resultado de uma ação confirmada ou recusada pelo usuário."""

    action: SpringMvcAction
    status: str
    message: str


@dataclass
class SpringMvcPlan:
    """Plano seguro e incremental para aplicar estrutura MVC em um projeto Spring."""

    project_path: Path
    package_name: str
    is_valid_project: bool
    is_spring_boot_project: bool
    actions: list[SpringMvcAction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def can_apply(self) -> bool:
        return self.is_valid_project and self.is_spring_boot_project and bool(self.actions)
