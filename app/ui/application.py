from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Input, Label, OptionList, Select, Static
from textual.widgets.option_list import Option

from app.generator import ProjectGenerationError, ProjectGenerator
from app.models.detect_project import DetectedProject, Technology
from app.models.project_config import ProjectConfig
from app.workflow.open_project_workflow import OpenProjectWorkflow


STACK_BASE_LOGO = r"""
███████╗████████╗ █████╗  ██████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
███████╗   ██║   ███████║██║     █████╔╝
╚════██║   ██║   ██╔══██║██║     ██╔═██╗
███████║   ██║   ██║  ██║╚██████╗██║  ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                     BASE
"""

STACK_OPTIONS = [
    ("Java + Spring Boot", "Java + Spring Boot"),
    ("Python + FastAPI", "Python + FastAPI"),
    ("Node.js + NestJS", "Node.js + NestJS"),
]

ARCHITECTURE_OPTIONS = [
    ("MVC", "MVC"),
    ("Clean Architecture", "Clean Architecture"),
    ("Hexagonal", "Hexagonal"),
]

DATABASE_OPTIONS = [
    ("PostgreSQL", "PostgreSQL"),
    ("MySQL", "MySQL"),
    ("H2", "H2"),
    ("Sem banco de dados", "Sem banco de dados"),
]

BOOLEAN_OPTIONS = [("Sim", "yes"), ("Não", "no")]


class StackBaseApp(App[None]):
    """Aplicação TUI principal do Stack Base."""

    TITLE = "Stack Base"
    CSS_PATH = "stack_base.tcss"

    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("escape", "back", "Voltar"),
        Binding("h", "home", "Início"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.generator = ProjectGenerator()
        self.open_project_workflow = OpenProjectWorkflow()

    def compose(self) -> ComposeResult:
        """Monta todos os painéis da TUI e exibe o início por padrão."""

        with Container(id="screen-container"):
            yield from self._compose_home()
            yield from self._compose_create_project()
            yield from self._compose_templates()
            yield from self._compose_validate_project()
            yield from self._compose_devsecops()
            yield from self._compose_settings()
            yield from self._compose_about()

    def _compose_home(self) -> ComposeResult:
        with Vertical(id="home", classes="panel"):
            yield Static(STACK_BASE_LOGO, id="logo")
            yield Label("Crie projetos padronizados sem começar do zero.", id="description")
            yield Label("Selecione uma opção", id="menu-title")
            yield OptionList(
                Option("Criar novo projeto", id="create-project"),
                Option("Explorar templates", id="templates"),
                Option("Validar projeto", id="validate-project"),
                Option("DevSecOps / Oneflow", id="devsecops"),
                Option("Configurações", id="settings"),
                Option("Sobre", id="about"),
                Option("Sair", id="exit"),
                id="main-menu",
            )
            yield Static("↑ ↓ navegar   •   Enter selecionar   •   Esc voltar   •   Q sair", id="help")

    def _compose_create_project(self) -> ComposeResult:
        with Vertical(id="create-view", classes="panel hidden"):
            yield Label("Criar novo projeto", classes="screen-title")
            yield Label("Preencha as opções abaixo e gere um scaffold inicial funcional.")
            yield Input(placeholder="Nome do projeto", id="create-name")
            yield Input(value=str(Path.cwd()), placeholder="Diretório de saída", id="create-output")
            yield Select(STACK_OPTIONS, prompt="Stack", id="create-stack")
            yield Select(ARCHITECTURE_OPTIONS, prompt="Arquitetura", id="create-architecture")
            yield Select(DATABASE_OPTIONS, prompt="Banco de dados", id="create-database")
            with Horizontal(classes="form-row"):
                yield Select(BOOLEAN_OPTIONS, prompt="Docker", id="create-docker")
                yield Select(BOOLEAN_OPTIONS, prompt="Testes", id="create-tests")
                yield Select(BOOLEAN_OPTIONS, prompt="CI/CD", id="create-ci")
            with Horizontal(classes="actions"):
                yield Button("Gerar projeto", id="generate-project", variant="success")
                yield Button("Voltar", id="back-home-create")
            yield Static("", id="create-result", classes="result-box")

    def _compose_templates(self) -> ComposeResult:
        with Vertical(id="templates-view", classes="panel hidden"):
            yield Label("Templates disponíveis", classes="screen-title")
            yield Static(
                """┌────────────────────────┬──────────────────────┬────────────────────┬────────────┐
│ Template               │ Stack                │ Arquitetura       │ Status     │
├────────────────────────┼──────────────────────┼────────────────────┼────────────┤
│ java-spring-mvc        │ Java + Spring Boot   │ MVC                │ Pronto     │
│ java-spring-clean      │ Java + Spring Boot   │ Clean Architecture │ Pronto     │
│ java-spring-hexagonal  │ Java + Spring Boot   │ Hexagonal          │ Pronto     │
│ python-fastapi-service │ Python + FastAPI     │ MVC                │ Pronto     │
│ node-nest-service      │ Node.js + NestJS     │ Modular            │ Pronto     │
└────────────────────────┴──────────────────────┴────────────────────┴────────────┘""",
                classes="table-box",
            )
            yield Static("Todos os templates geram README, .gitignore e project-config.yaml.")
            yield Button("Voltar", id="back-home-templates")

    def _compose_validate_project(self) -> ComposeResult:
        with Vertical(id="validate-view", classes="panel hidden"):
            yield Label("Validar projeto existente", classes="screen-title")
            yield Label("Informe um diretório para detectar Java, Spring, build tools, Docker e testes.")
            yield Input(value=str(Path.cwd()), placeholder="Caminho do projeto", id="validate-path")
            with Horizontal(classes="actions"):
                yield Button("Executar validação", id="run-validation", variant="primary")
                yield Button("Voltar", id="back-home-validate")
            yield Static("", id="validation-result", classes="result-box")

    def _compose_devsecops(self) -> ComposeResult:
        with Vertical(id="devsecops-view", classes="panel hidden"):  # pragma: no cover - layout only
            yield Label("DevSecOps / Oneflow Datasus", classes="screen-title")
            yield Static(
                """Branches:
• main: versão de produção.
• develop: base de desenvolvimento e branch padrão para análise estática.
• feat/<funcionalidade>: implementação isolada para integração via rebase + fast-forward.

Tags e ambientes:
• dev-feat-<funcionalidade>-N: validação de feature.
• dev-vX.Y.Z: deploy em desenvolvimento.
• hmg-vX.Y.Z-rcN: candidata para homologação.
• vX.Y.Z: produção, no mesmo commit aprovado em homologação.

Quality/Security gates:
• build e testes unitários em Merge Request.
• análise estática, cobertura e dependency scan.
• SAST/Trivy em CI; DAST/OWASP ZAP em ambientes implantados.
• code review obrigatório antes da integração.

Rastreabilidade:
• a tag Git deve ser idêntica à tag da imagem de container implantada.""",
                classes="result-box",
            )
            yield Button("Voltar", id="back-home-devsecops")

    def _compose_settings(self) -> ComposeResult:
        with Vertical(id="settings-view", classes="panel hidden"):
            yield Label("Configurações", classes="screen-title")
            yield Static(
                """Configurações do MVP:

• Tema: carmesim escuro
• Diretório padrão de saída: diretório atual da execução
• Templates locais: Java Spring, Python FastAPI e Node NestJS
• Validação local: sem chamadas externas e sem telemetria

As próximas versões podem persistir preferências por usuário e organização.""",
                classes="result-box",
            )
            yield Button("Voltar", id="back-home-settings")

    def _compose_about(self) -> ComposeResult:
        with Vertical(id="about-view", classes="panel hidden"):
            yield Label("Sobre", classes="screen-title")
            yield Static(
                """Stack Base 0.1.0

Ferramenta interativa de terminal para criar, detectar, validar e padronizar projetos de software.

Este MVP entrega uma TUI navegável, geração inicial de projetos e validação básica de projetos existentes.""",
                classes="result-box",
            )
            yield Button("Voltar", id="back-home-about")

    def on_mount(self) -> None:
        """Coloca o foco no menu ao iniciar."""

        self._show_panel("home")
        self.query_one("#main-menu", OptionList).focus()

    def _show_panel(self, panel_id: str) -> None:
        for panel in self.query(".panel"):
            panel.display = panel.id == panel_id

    def action_home(self) -> None:
        self._show_panel("home")
        self.query_one("#main-menu", OptionList).focus()

    def action_back(self) -> None:
        self.action_home()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option_id = event.option.id

        if option_id == "exit":
            self.action_quit()
            return

        panel_by_option = {
            "create-project": "create-view",
            "templates": "templates-view",
            "validate-project": "validate-view",
            "devsecops": "devsecops-view",
            "settings": "settings-view",
            "about": "about-view",
        }

        panel_id = panel_by_option.get(str(option_id))
        if panel_id is not None:
            self._show_panel(panel_id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id and button_id.startswith("back-home"):
            self.action_home()
            return

        if button_id == "generate-project":
            self._generate_project()
            return

        if button_id == "run-validation":
            self._validate_project()

    def _generate_project(self) -> None:
        result = self.query_one("#create-result", Static)
        name = self.query_one("#create-name", Input).value.strip()
        output = self.query_one("#create-output", Input).value.strip() or str(Path.cwd())

        config = ProjectConfig(
            name=name,
            output_directory=Path(output).expanduser(),
            stack=self._select_value("#create-stack", "Java + Spring Boot"),
            architecture=self._select_value("#create-architecture", "MVC"),
            database=self._select_value("#create-database", "Sem banco de dados"),
            use_docker=self._select_value("#create-docker", "yes") == "yes",
            use_tests=self._select_value("#create-tests", "yes") == "yes",
            use_ci=self._select_value("#create-ci", "no") == "yes",
        )

        try:
            project_path = self.generator.generate(config)
        except ProjectGenerationError as error:
            result.update(f"❌ {error}")
            return
        except OSError as error:
            result.update(f"❌ Não foi possível escrever os arquivos: {error}")
            return

        result.update(
            f"✅ Projeto gerado com sucesso em:\n{project_path}\n\n"
            "Arquivos base: README.md, .gitignore, project-config.yaml e estrutura da stack."
        )

    def _validate_project(self) -> None:
        result_widget = self.query_one("#validation-result", Static)
        path = self.query_one("#validate-path", Input).value.strip() or str(Path.cwd())
        detected_project = self.open_project_workflow.execute(path)
        result_widget.update(self._format_detected_project(detected_project))

    def _select_value(self, selector: str, default: str) -> str:
        value = self.query_one(selector, Select).value
        if value == Select.NULL:
            return default
        return str(value)

    @staticmethod
    def _format_detected_project(project: DetectedProject) -> str:
        lines = [
            f"Projeto: {project.name}",
            f"Caminho: {project.root_path}",
            f"Diretório válido: {'sim' if project.is_valid_project else 'não'}",
            "",
            f"Linguagens: {StackBaseApp._join_technologies(project.languages)}",
            f"Frameworks: {StackBaseApp._join_technologies(project.frameworks)}",
            f"Build tools: {StackBaseApp._join_technologies(project.build_tools)}",
            f"Capacidades: {StackBaseApp._join_technologies(project.capabilities)}",
            f"Providers: {StackBaseApp._join_technologies(project.providers)}",
            f"Arquivos detectados: {', '.join(project.detected_files) or 'nenhum'}",
        ]

        if project.warnings:
            lines.extend(["", "Avisos:", *[f"• {warning}" for warning in project.warnings]])

        return "\n".join(lines)

    @staticmethod
    def _join_technologies(technologies: list[Technology]) -> str:
        return ", ".join(technology.name for technology in technologies) or "nenhuma"


def run() -> None:
    """Executa a aplicação Textual."""

    StackBaseApp().run()
