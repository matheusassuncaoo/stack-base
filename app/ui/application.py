from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Label, OptionList, Static
from textual.widgets.option_list import Option


STACK_BASE_LOGO = r"""
███████╗████████╗ █████╗  ██████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
███████╗   ██║   ███████║██║     █████╔╝
╚════██║   ██║   ██╔══██║██║     ██╔═██╗
███████║   ██║   ██║  ██║╚██████╗██║  ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                     BASE
"""


class StackBaseApp(App[None]):
    """Aplicação principal do Stack Base."""

    TITLE = "Stack Base"

    CSS_PATH = "stack_base.tcss"

    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("escape", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        """Monta a tela inicial."""

        with Container(id="screen-container"):
            with Vertical(id="home"):
                yield Static(
                    STACK_BASE_LOGO,
                    id="logo",
                )

                yield Label(
                    "Crie projetos padronizados sem começar do zero.",
                    id="description",
                )

                yield Label(
                    "Selecione uma opção",
                    id="menu-title",
                )

                yield OptionList(
                    Option(
                        "Criar novo projeto",
                        id="create-project",
                    ),
                    Option(
                        "Explorar templates",
                        id="templates",
                    ),
                    Option(
                        "Validar projeto",
                        id="validate-project",
                    ),
                    Option(
                        "Configurações",
                        id="settings",
                    ),
                    Option(
                        "Sobre",
                        id="about",
                    ),
                    Option(
                        "Sair",
                        id="exit",
                    ),
                    id="main-menu",
                )

                yield Static(
                    "↑ ↓ navegar   •   Enter selecionar   •   Q sair",
                    id="help",
                )

    def on_mount(self) -> None:
        """Coloca o foco no menu."""

        self.query_one(
            "#main-menu",
            OptionList,
        ).focus()

    def on_option_list_option_selected(
        self,
        event: OptionList.OptionSelected,
    ) -> None:
        """Executa a opção selecionada."""

        option_id = event.option.id

        actions = {
            "create-project": self.action_create_project,
            "templates": self.action_templates,
            "validate-project": self.action_validate_project,
            "settings": self.action_settings,
            "about": self.action_about,
            "exit": self.action_quit,
        }

        action = actions.get(option_id)

        if action is not None:
            action()

    def action_create_project(self) -> None:
        self.notify(
            "Tela de criação será implementada agora.",
            title="Criar projeto",
        )

    def action_templates(self) -> None:
        self.notify(
            "Catálogo de templates ainda não implementado.",
            title="Templates",
        )

    def action_validate_project(self) -> None:
        self.notify(
            "Validação ainda não implementada.",
            title="Validar projeto",
        )

    def action_settings(self) -> None:
        self.notify(
            "Configurações ainda não implementadas.",
            title="Configurações",
        )

    def action_about(self) -> None:
        self.notify(
            "Stack Base 0.1.0",
            title="Sobre",
        )


def run() -> None:
    """Executa a aplicação."""

    StackBaseApp().run()