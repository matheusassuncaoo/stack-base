from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static


class StackBaseApp(App):
    """Aplicação principal do Stack Base."""

    TITLE = "Stack Base"
    SUB_TITLE = "Project scaffolding and architecture standardization"

    CSS_PATH = "stack_base.tcss"

    BINDINGS = [
        ("q", "quit", "Sair"),
        ("c", "create_project", "Criar projeto"),
        ("t", "show_templates", "Templates"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="main-layout"):
            with Vertical(id="sidebar"):
                yield Label("STACK BASE", id="brand")

                yield ListView(
                    ListItem(Label("Criar projeto"), id="create-project"),
                    ListItem(Label("Templates"), id="templates"),
                    ListItem(Label("Validar projeto"), id="validate-project"),
                    ListItem(Label("Configurações"), id="settings"),
                    id="navigation",
                )

            with Vertical(id="content"):
                yield Static(
                    """
[bold]Bem-vindo ao Stack Base[/bold]

Crie, configure e valide projetos de software
utilizando estruturas padronizadas.

[bold]Stack inicial[/bold]
• Java
• Spring Boot
• MVC
• Docker
• Testes automatizados

Selecione uma opção no menu lateral.
                    """,
                    id="welcome",
                    markup=True,
                )

                yield Static(
                    """
[bold]Próximo projeto[/bold]

Nome: ainda não definido
Template: java-spring
Arquitetura: MVC
Status: aguardando configuração
                    """,
                    id="project-summary",
                    markup=True,
                )

        yield Footer()

    def action_create_project(self) -> None:
        self.notify(
            "A tela de criação será aberta.",
            title="Stack Base",
        )

    def action_show_templates(self) -> None:
        self.notify(
            "Abrindo catálogo de templates.",
            title="Stack Base",
        )


def run() -> None:
    StackBaseApp().run()