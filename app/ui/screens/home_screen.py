from app.ui.console import (
    clear_screen,
    draw_header,
    get_terminal_width,
    horizontal_line,
)


def show_home_screen() -> str:
    """
    Exibe a tela inicial e retorna a opção selecionada.
    """
    clear_screen()

    width = get_terminal_width()
    menu_width = 28
    content_width = width - menu_width - 5

    draw_header(
        title="STACK BASE",
        subtitle="Project scaffolding and architecture standardization",
    )

    menu_items = [
        "[1] Criar projeto",
        "[2] Templates",
        "[3] Validar projeto",
        "[4] Configurações",
        "[5] Sobre",
        "[0] Sair",
    ]

    content_lines = [
        "Bem-vindo ao Stack Base.",
        "",
        "Crie estruturas de projetos padronizadas sem repetir",
        "configurações, pastas e arquivos manualmente.",
        "",
        "Recursos planejados:",
        "  • Java + Spring Boot",
        "  • MVC, Clean e Hexagonal",
        "  • Docker",
        "  • Banco de dados",
        "  • Testes automatizados",
        "  • CI/CD",
        "  • Validação arquitetural",
        "",
        "Selecione uma opção no menu lateral.",
    ]

    max_lines = max(
        len(menu_items),
        len(content_lines),
    )

    print(
        "┌"
        + "─" * menu_width
        + "┬"
        + "─" * content_width
        + "┐"
    )

    menu_title = " MENU ".center(menu_width)
    content_title = " VISÃO GERAL ".center(content_width)

    print(
        f"│{menu_title}│{content_title}│"
    )

    print(
        "├"
        + "─" * menu_width
        + "┼"
        + "─" * content_width
        + "┤"
    )

    for index in range(max_lines):
        menu_text = (
            menu_items[index]
            if index < len(menu_items)
            else ""
        )

        content_text = (
            content_lines[index]
            if index < len(content_lines)
            else ""
        )

        print(
            f"│ {menu_text:<{menu_width - 2}}"
            f"│ {content_text:<{content_width - 2}}│"
        )

    print(
        "└"
        + "─" * menu_width
        + "┴"
        + "─" * content_width
        + "┘"
    )

    print(horizontal_line())

    return input("stackbase > ").strip()