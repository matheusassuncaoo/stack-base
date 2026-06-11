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
from app.workflow.spring_mvc_workflow import SpringMvcWorkflow


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
        self.spring_mvc_workflow = SpringMvcWorkflow()
        self._spring_mvc_plan = None
        self._spring_mvc_action_index = 0
        self._spring_mvc_log: list[str] = []

    def compose(self) -> ComposeResult:
        """Monta todos os painéis da TUI e exibe o início por padrão."""

        with Container(id="screen-container"):
            yield from self._compose_home()
            yield from self._compose_create_project()
            yield from self._compose_templates()
            yield from self._compose_validate_project()
            yield from self._compose_spring_mvc()
            yield from self._compose_validate_modal()
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
                Option("Estruturar Spring MVC", id="spring-mvc"),
                Option("Configurações", id="settings"),
                Option("Sobre", id="about"),
                Option("Sair", id="exit"),
                id="main-menu",
            )
            yield Static(
                "↑ ↓ navegar   •   Enter selecionar   •   Esc voltar   •   Q sair", id="help"
            )

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
            yield Label(
                "Informe um diretório para detectar Java, Spring, build tools, Docker e testes."
            )
            yield Input(value=str(Path.cwd()), placeholder="Caminho do projeto", id="validate-path")
            with Horizontal(classes="actions"):
                yield Button("Executar validação", id="run-validation", variant="primary")
                yield Button("Voltar", id="back-home-validate")
            yield Static("", id="validation-result", classes="result-box")

    def _compose_spring_mvc(self) -> ComposeResult:
        with Vertical(id="spring-mvc-view", classes="panel hidden"):
            yield Label("Estruturar Spring MVC", classes="screen-title")
            yield Label(
                "Escolha um projeto Spring Boot existente. O Stack Base valida, planeja e só aplica cada item após sua confirmação."
            )
            yield Input(
                value=str(Path.cwd()),
                placeholder="Caminho do projeto Spring Boot",
                id="spring-mvc-path",
            )
            with Horizontal(classes="actions"):
                yield Button("Analisar MVC", id="analyze-spring-mvc", variant="primary")
                yield Button(
                    "Aplicar próxima ação", id="apply-spring-mvc-action", variant="success"
                )
                yield Button("Negar próxima ação", id="skip-spring-mvc-action")
                yield Button("Voltar", id="back-home-spring-mvc")
            yield Static("", id="spring-mvc-result", classes="result-box")

    def _compose_validate_modal(self) -> ComposeResult:
        """Modal interno usado para exibir o resultado da validação sem abrir uma janela externa."""
        with Vertical(id="validate-modal", classes="panel hidden"):
            yield Label("Resultado da validação", classes="screen-title")
            yield Static("", id="validate-modal-body", classes="result-box")
            yield Button("Fechar", id="close-validate-modal")

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
            "spring-mvc": "spring-mvc-view",
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
            return

        if button_id == "analyze-spring-mvc":
            self._analyze_spring_mvc()
            return

        if button_id == "apply-spring-mvc-action":
            self._handle_next_spring_mvc_action(approved=True)
            return

        if button_id == "skip-spring-mvc-action":
            self._handle_next_spring_mvc_action(approved=False)
            return

        if button_id == "close-validate-modal":
            # Esconde o modal de validação
            try:
                self.query_one("#validate-modal", Vertical).display = False
            except Exception:
                pass
            return

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
        # Executa a detecção e exibe o resultado dentro de um modal interno na TUI
        path = self.query_one("#validate-path", Input).value.strip() or str(Path.cwd())
        detected_project = self.open_project_workflow.execute(path)
        body = self._format_detected_project(detected_project)

        # Preenche o conteúdo do modal e mostra-o
        try:
            self.query_one("#validate-modal-body", Static).update(body)
            self.query_one("#validate-modal", Vertical).display = True
            # Foca no botão fechar para acessibilidade/teclado
            self.query_one("#close-validate-modal", Button).focus()
        except Exception:
            # Fallback: atualiza a área padrão se algo falhar
            self.query_one("#validation-result", Static).update(body)

    def _analyze_spring_mvc(self) -> None:
        path = self.query_one("#spring-mvc-path", Input).value.strip() or str(Path.cwd())
        self._spring_mvc_plan = self.spring_mvc_workflow.plan(path)
        self._spring_mvc_action_index = 0
        self._spring_mvc_log = []
        self._render_spring_mvc_state()

    def _handle_next_spring_mvc_action(self, approved: bool) -> None:
        result = self.query_one("#spring-mvc-result", Static)

        if self._spring_mvc_plan is None:
            result.update("Analise um projeto Spring Boot antes de executar ações MVC.")
            return

        if self._spring_mvc_action_index >= len(self._spring_mvc_plan.actions):
            self._render_spring_mvc_state()
            return

        action = self._spring_mvc_plan.actions[self._spring_mvc_action_index]
        self._spring_mvc_action_index += 1

        if approved:
            action_result = self.spring_mvc_workflow.apply_action(
                self._spring_mvc_plan.project_path,
                action,
            )
            self._spring_mvc_log.append(f"✅ {action.relative_path}: {action_result.message}")
        else:
            self._spring_mvc_log.append(f"↩ {action.relative_path}: ação negada pelo usuário.")

        self._render_spring_mvc_state()

    def _render_spring_mvc_state(self) -> None:
        result = self.query_one("#spring-mvc-result", Static)

        if self._spring_mvc_plan is None:
            result.update("")
            return

        plan = self._spring_mvc_plan
        lines = [
            f"Projeto: {plan.project_path}",
            f"Pacote base: {plan.package_name}",
            f"Diretório válido: {'sim' if plan.is_valid_project else 'não'}",
            f"Spring Boot detectado: {'sim' if plan.is_spring_boot_project else 'não'}",
            "",
        ]

        if plan.warnings:
            lines.extend(["Avisos:", *[f"• {warning}" for warning in plan.warnings], ""])

        if plan.actions:
            lines.append("Ações MVC planejadas:")
            for index, action in enumerate(plan.actions, start=1):
                prefix = "→" if index - 1 == self._spring_mvc_action_index else " "
                lines.append(f"{prefix} {index}. {action.description} ({action.relative_path})")
        else:
            lines.append("Nenhuma ação MVC pendente.")

        if self._spring_mvc_action_index < len(plan.actions):
            current_action = plan.actions[self._spring_mvc_action_index]
            lines.extend(
                [
                    "",
                    "Próxima decisão do usuário:",
                    f"{current_action.description}",
                    f"Destino: {current_action.relative_path}",
                ]
            )
        elif plan.actions:
            lines.extend(["", "Todas as ações planejadas foram confirmadas ou negadas."])

        if self._spring_mvc_log:
            lines.extend(["", "Histórico:", *self._spring_mvc_log])

        result.update("\n".join(lines))

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
