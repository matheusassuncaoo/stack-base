from collections.abc import Callable
from pathlib import Path

from app.models.spring_mvc import SpringMvcAction, SpringMvcActionResult, SpringMvcPlan
from app.validation.project_detector import ProjectDetector


class SpringMvcWorkflow:
    """Planeja e aplica a estrutura MVC em projetos Java Spring Boot existentes."""

    def __init__(self, detector: ProjectDetector | None = None) -> None:
        self.detector = detector or ProjectDetector()

    def plan(self, project_path: str | Path) -> SpringMvcPlan:
        root_path = Path(project_path).expanduser().resolve()
        detected_project = self.detector.detect(root_path)
        is_spring_boot = any(
            framework.name == "Spring Boot" for framework in detected_project.frameworks
        )
        package_name = self._detect_base_package(root_path)
        package_path = Path(*package_name.split("."))
        java_root = Path("src/main/java") / package_path

        plan = SpringMvcPlan(
            project_path=root_path,
            package_name=package_name,
            is_valid_project=detected_project.is_valid_project,
            is_spring_boot_project=is_spring_boot,
        )

        if not detected_project.is_valid_project:
            plan.warnings.extend(detected_project.warnings or ["Projeto informado não é válido."])
            return plan

        if not is_spring_boot:
            plan.warnings.append(
                "A estrutura MVC só pode ser aplicada após identificar um projeto Spring Boot."
            )
            return plan

        planned_directories = [
            (java_root / "controller", "Criar camada de controllers HTTP."),
            (java_root / "service", "Criar camada de serviços de aplicação."),
            (java_root / "repository", "Criar camada de repositórios."),
            (java_root / "model", "Criar camada de modelos/entidades."),
            (java_root / "dto", "Criar camada de DTOs para entrada e saída."),
            (Path("src/main/resources/templates"), "Criar pasta de views/templates."),
            (Path("src/main/resources/static"), "Criar pasta de assets estáticos."),
        ]

        for relative_path, description in planned_directories:
            if not (root_path / relative_path).exists():
                plan.actions.append(
                    SpringMvcAction(
                        relative_path=relative_path,
                        description=description,
                        action_type="directory",
                    )
                )

        planned_files = self._sample_files(java_root, package_name)
        for action in planned_files:
            if not (root_path / action.relative_path).exists():
                plan.actions.append(action)

        if not plan.actions:
            plan.warnings.append("Nenhuma ação pendente: o projeto já possui a base MVC esperada.")

        return plan

    def execute(
        self,
        project_path: str | Path,
        confirm_action: Callable[[SpringMvcAction], bool],
    ) -> tuple[SpringMvcPlan, list[SpringMvcActionResult]]:
        plan = self.plan(project_path)
        results: list[SpringMvcActionResult] = []

        if not plan.can_apply:
            return plan, results

        for action in plan.actions:
            if not confirm_action(action):
                results.append(
                    SpringMvcActionResult(
                        action=action,
                        status="skipped",
                        message="Ação recusada pelo usuário.",
                    )
                )
                continue

            results.append(self.apply_action(plan.project_path, action))

        return plan, results

    @staticmethod
    def apply_action(project_path: Path, action: SpringMvcAction) -> SpringMvcActionResult:
        target_path = project_path / action.relative_path

        if target_path.exists():
            return SpringMvcActionResult(
                action=action,
                status="skipped",
                message="Item já existe; nada foi sobrescrito.",
            )

        if action.action_type == "directory":
            target_path.mkdir(parents=True, exist_ok=True)
            return SpringMvcActionResult(
                action=action, status="created", message="Diretório criado."
            )

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(action.content or "", encoding="utf-8")
        return SpringMvcActionResult(action=action, status="created", message="Arquivo criado.")

    @staticmethod
    def _detect_base_package(root_path: Path) -> str:
        java_files = sorted((root_path / "src/main/java").rglob("*.java"))

        for java_file in java_files:
            try:
                content = java_file.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            if "@SpringBootApplication" not in content:
                continue

            for line in content.splitlines():
                stripped_line = line.strip()
                if stripped_line.startswith("package ") and stripped_line.endswith(";"):
                    return stripped_line.removeprefix("package ").removesuffix(";").strip()

        return "com.example.app"

    @staticmethod
    def _sample_files(java_root: Path, package_name: str) -> list[SpringMvcAction]:
        return [
            SpringMvcAction(
                relative_path=java_root / "controller" / "HomeController.java",
                description="Criar HomeController com endpoint inicial de saúde da camada web.",
                action_type="file",
                content=f"""package {package_name}.controller;\n\nimport org.springframework.stereotype.Controller;\nimport org.springframework.web.bind.annotation.GetMapping;\nimport org.springframework.web.bind.annotation.ResponseBody;\n\n@Controller\npublic class HomeController {{\n    @GetMapping("/")\n    @ResponseBody\n    public String index() {{\n        return "Spring MVC estruturado pelo Stack Base";\n    }}\n}}\n""",
            ),
            SpringMvcAction(
                relative_path=java_root / "service" / "HomeService.java",
                description="Criar HomeService como ponto inicial da camada de serviços.",
                action_type="file",
                content=f"""package {package_name}.service;\n\nimport org.springframework.stereotype.Service;\n\n@Service\npublic class HomeService {{\n    public String message() {{\n        return "ok";\n    }}\n}}\n""",
            ),
        ]
