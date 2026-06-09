from dataclasses import dataclass

from app.ui.console import (
    clear_screen,
    draw_header,
    horizontal_line,
    wait_for_enter,
)


@dataclass(frozen=True)
class ProjectPreview:
    name: str
    stack: str
    architecture: str
    database: str
    use_docker: bool
    use_tests: bool
    use_ci: bool


STACK_OPTIONS = {
    "1": "Java + Spring Boot",
    "2": "Python + FastAPI",
    "3": "Node.js + NestJS",
}

ARCHITECTURE_OPTIONS = {
    "1": "MVC",
    "2": "Clean Architecture",
    "3": "Hexagonal",
}

DATABASE_OPTIONS = {
    "1": "PostgreSQL",
    "2": "MySQL",
    "3": "H2",
    "4": "Sem banco de dados",
}


def ask_option(
    title: str,
    options: dict[str, str],
) -> str:
    """
    Solicita uma opção válida ao usuário.
    """
    while True:
        print(f"\n{title}")

        for key, value in options.items():
            print(f"[{key}] {value}")

        selected_option = input("\nSelecione: ").strip()

        if selected_option in options:
            return options[selected_option]

        print("\nOpção inválida. Tente novamente.")


def ask_boolean(
    label: str,
    default: bool = True,
) -> bool:
    """
    Solicita uma confirmação no formato sim ou não.
    """
    suffix = "[S/n]" if default else "[s/N]"

    answer = input(
        f"{label} {suffix}: ",
    ).strip().lower()

    if not answer:
        return default

    return answer in {
        "s",
        "sim",
        "y",
        "yes",
    }


def show_create_screen() -> None:
    """
    Exibe o fluxo interativo de criação de projeto.
    """
    clear_screen()

    draw_header(
        title="STACK BASE",
        subtitle="Criar novo projeto",
    )

    project_name = input(
        "Nome do projeto: ",
    ).strip()

    if not project_name:
        print("\nO nome do projeto é obrigatório.")
        wait_for_enter()
        return

    stack = ask_option(
        title="Selecione a stack:",
        options=STACK_OPTIONS,
    )

    architecture = ask_option(
        title="Selecione a arquitetura:",
        options=ARCHITECTURE_OPTIONS,
    )

    database = ask_option(
        title="Selecione o banco de dados:",
        options=DATABASE_OPTIONS,
    )

    print()

    use_docker = ask_boolean(
        "Adicionar Docker?",
    )

    use_tests = ask_boolean(
        "Adicionar testes?",
    )

    use_ci = ask_boolean(
        "Adicionar pipeline de CI/CD?",
        default=False,
    )

    preview = ProjectPreview(
        name=project_name,
        stack=stack,
        architecture=architecture,
        database=database,
        use_docker=use_docker,
        use_tests=use_tests,
        use_ci=use_ci,
    )

    show_project_preview(preview)


def show_project_preview(
    preview: ProjectPreview,
) -> None:
    """
    Exibe uma prévia visual do projeto escolhido.
    """
    clear_screen()

    draw_header(
        title="STACK BASE",
        subtitle="Prévia da geração",
    )

    print("CONFIGURAÇÃO")
    print(horizontal_line())
    print(f"Projeto:       {preview.name}")
    print(f"Stack:         {preview.stack}")
    print(f"Arquitetura:   {preview.architecture}")
    print(f"Banco:         {preview.database}")
    print(
        f"Docker:        {'Sim' if preview.use_docker else 'Não'}"
    )
    print(
        f"Testes:        {'Sim' if preview.use_tests else 'Não'}"
    )
    print(
        f"CI/CD:         {'Sim' if preview.use_ci else 'Não'}"
    )

    print()
    print("ESTRUTURA PREVISTA")
    print(horizontal_line())

    show_structure_tree(preview)

    print(horizontal_line())

    confirm = ask_boolean(
        "Confirmar geração?",
    )

    if confirm:
        print()
        print(
            f"Projeto '{preview.name}' preparado para geração."
        )
        print(
            "O gerador de arquivos será implementado no próximo passo."
        )
    else:
        print("\nGeração cancelada.")

    wait_for_enter()


def show_structure_tree(
    preview: ProjectPreview,
) -> None:
    """
    Exibe uma estrutura aproximada baseada na configuração.
    """
    print(f"{preview.name}/")
    print("├── src/")
    print("│   ├── main/")
    print("│   └── test/" if preview.use_tests else "│")
    print("├── README.md")
    print("├── .gitignore")

    if preview.use_docker:
        print("├── Dockerfile")
        print("├── docker-compose.yml")

    if preview.use_ci:
        print("├── .github/")
        print("│   └── workflows/")
        print("│       └── build.yml")

    print("└── project-config.yaml")