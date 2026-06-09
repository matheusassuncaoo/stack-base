from app.ui.console import (
    clear_screen,
    draw_header,
    horizontal_line,
    wait_for_enter,
)


def show_about_screen() -> None:
    """
    Exibe informações sobre o Stack Base.
    """
    clear_screen()

    draw_header(
        title="STACK BASE",
        subtitle="Sobre o projeto",
    )

    print("Versão: 0.1.0")
    print("Licença: MIT")
    print("Linguagem: Python")
    print()

    print(horizontal_line())

    print(
        "Stack Base é uma ferramenta interativa de terminal "
        "para criar, padronizar, validar e evoluir projetos "
        "de software."
    )

    print()
    print(
        "O objetivo é reduzir tarefas repetitivas relacionadas "
        "à criação de estruturas, configurações, documentação, "
        "testes e recursos de infraestrutura."
    )

    wait_for_enter()