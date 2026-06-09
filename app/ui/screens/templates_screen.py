from app.ui.console import (
    clear_screen,
    draw_header,
    horizontal_line,
    wait_for_enter,
)


def show_templates_screen() -> None:
    """
    Exibe os templates disponíveis.
    """
    clear_screen()

    draw_header(
        title="STACK BASE",
        subtitle="Templates disponíveis",
    )

    templates = [
        {
            "name": "java-spring-mvc",
            "stack": "Java + Spring Boot",
            "architecture": "MVC",
            "status": "Planejado",
        },
        {
            "name": "java-spring-clean",
            "stack": "Java + Spring Boot",
            "architecture": "Clean Architecture",
            "status": "Planejado",
        },
        {
            "name": "java-spring-hexagonal",
            "stack": "Java + Spring Boot",
            "architecture": "Hexagonal",
            "status": "Planejado",
        },
    ]

    print(
        f"{'TEMPLATE':<28}"
        f"{'STACK':<25}"
        f"{'ARQUITETURA':<22}"
        f"{'STATUS':<12}"
    )

    print(horizontal_line())

    for template in templates:
        print(
            f"{template['name']:<28}"
            f"{template['stack']:<25}"
            f"{template['architecture']:<22}"
            f"{template['status']:<12}"
        )

    wait_for_enter()