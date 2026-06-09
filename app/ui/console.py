import os
import shutil


def clear_screen() -> None:
    """
    Limpa o terminal no Windows, Linux ou macOS.
    """
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def get_terminal_width(default: int = 100) -> int:
    """
    Retorna a largura atual do terminal.
    """
    terminal_size = shutil.get_terminal_size(
        fallback=(default, 30),
    )

    return max(terminal_size.columns, 70)


def horizontal_line(
    character: str = "─",
    width: int | None = None,
) -> str:
    """
    Cria uma linha horizontal baseada na largura do terminal.
    """
    current_width = width or get_terminal_width()

    return character * current_width


def center_text(
    text: str,
    width: int | None = None,
) -> str:
    """
    Centraliza um texto considerando a largura do terminal.
    """
    current_width = width or get_terminal_width()

    return text.center(current_width)


def truncate_text(
    text: str,
    width: int,
) -> str:
    """
    Limita um texto para evitar quebra indesejada no terminal.
    """
    if len(text) <= width:
        return text

    if width <= 3:
        return text[:width]

    return f"{text[: width - 3]}..."


def draw_header(
    title: str,
    subtitle: str = "",
) -> None:
    """
    Desenha o cabeçalho principal da aplicação.
    """
    width = get_terminal_width()

    print("┌" + "─" * (width - 2) + "┐")
    print(
        "│"
        + center_text(
            title,
            width - 2,
        )
        + "│"
    )

    if subtitle:
        print(
            "│"
            + center_text(
                subtitle,
                width - 2,
            )
            + "│"
        )

    print("└" + "─" * (width - 2) + "┘")


def wait_for_enter(
    message: str = "Pressione Enter para continuar...",
) -> None:
    """
    Pausa a execução até o usuário pressionar Enter.
    """
    input(f"\n{message}")