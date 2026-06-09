from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Container, Vertical
from textual.widgets import Footer, Label, OptionList, Static
from textual.widgets.option_list import Option


STACK_BASE_LOGO = r"""
 ███████╗████████╗ █████╗  ██████╗██╗  ██╗
 ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝
 ███████╗   ██║   ███████║██║     █████╔╝
 ╚════██║   ██║   ██╔══██║██║     ██╔═██╗
 ███████║   ██║   ██║  ██║╚██████╗██║  ██╗
 ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

 ██████╗  █████╗ ███████╗███████╗
 ██╔══██╗██╔══██╗██╔════╝██╔════╝
 ██████╔╝███████║███████╗█████╗
 ██╔══██╗██╔══██║╚════██║██╔══╝
 ██████╔╝██║  ██║███████║███████╗
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
"""


class StackBaseApp(App[None]):
    """Aplicação principal do Stack Base."""

    TITLE = "Stack Base"
    SUB_TITLE = "Project Scaffolding"

    CSS_PATH = "stack_base.tcss"

    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("escape", "quit", "Sair"),
    ]

    def compose(self) -> ComposeResult:
        """Monta a tela inicial uma única vez."""

        with Container(id="application-shell"):
            with Center(id="main-center"):
                with Vertical(id="home-container"):
                    yield Static(
                        STACK_BASE_LOGO,
                        id="logo",
                    )

                    yield Label(
                        "Gere e padronize projetos de software.",
                        id="subtitle",
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
                            "Validar projeto existente",
                            id="validate-project",
                        ),
                        Option(
                            "Configurações",
                            id="settings",
                        ),
                        Option(
                            "Sobre o Stack Base",
                            id="about",
                        ),
                        Option(
                            "Sair",
                            id="exit",
                        ),
                        id="main-menu",
                    )

                    yield Static(
                        "↑/↓ navegar    Enter selecionar    Q sair",
                        id="navigation-help",
                    )

        yield Footer()

    def on_mount(self) -> None:
        """Coloca o foco no menu principal."""

        menu = self.query_one("#main-menu", OptionList)
        menu.focus()

    def on_option_list_option_selected(
        self,
        event: OptionList.OptionSelected,
    ) -> None:
        """Executa a opção confirmada pelo usuário."""

        option_id = event.option.id

        if option_id == "create-project":
            self.action_create_project()
            return

        if option_id == "templates":
            self.action_templates()
            return

        if option_id == "validate-project":
            self.action_validate_project()
            return

        if option_id == "settings":
            self.action_settings()
            return

        if option_id == "about":
            self.action_about()
            return

        if option_id == "exit":
            self.exit()

    def action_create_project(self) -> None:
        self.notify(
            "A tela de criação será implementada em seguida.",
            title="Criar projeto",
        )

    def action_templates(self) -> None:
        self.notify(
            "O catálogo de templates será aberto aqui.",
            title="Templates",
        )

    def action_validate_project(self) -> None:
        self.notify(
            "O validador de projetos será aberto aqui.",
            title="Validação",
        )

    def action_settings(self) -> None:
        self.notify(
            "As configurações serão abertas aqui.",
            title="Configurações",
        )

    def action_about(self) -> None:
        self.notify(
            (
                "Stack Base 0.1.0 — ferramenta para geração "
                "e padronização de projetos."
            ),
            title="Sobre",
        )


def run() -> None:
    """Executa a interface do Stack Base."""

    StackBaseApp().run()