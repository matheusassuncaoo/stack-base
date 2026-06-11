from pathlib import Path

import typer

from app.models.spring_mvc import SpringMvcAction
from app.ui.application import run
from app.workflow.spring_mvc_workflow import SpringMvcWorkflow

app = typer.Typer(
    name="stackbase",
    help="Gera, padroniza e valida projetos de software em uma TUI.",
    invoke_without_command=True,
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Inicializa a TUI quando nenhum subcomando for informado."""

    if ctx.invoked_subcommand is None:
        run()


@app.command()
def version() -> None:
    """Exibe a versão atual do Stack Base."""

    typer.echo("Stack Base versão 0.1.0")


@app.command("spring-mvc")
def spring_mvc(
    project_path: Path = typer.Argument(
        ...,
        help="Diretório do projeto Spring Boot existente que será estruturado como MVC.",
    ),
) -> None:
    """Estrutura um projeto Spring Boot existente no padrão MVC com confirmação por etapa."""

    workflow = SpringMvcWorkflow()
    plan = workflow.plan(project_path)

    typer.echo("Stack Base • Estruturação Spring MVC")
    typer.echo(f"Projeto: {plan.project_path}")
    typer.echo(f"Pacote base: {plan.package_name}")
    typer.echo(f"Projeto válido: {'sim' if plan.is_valid_project else 'não'}")
    typer.echo(f"Spring Boot detectado: {'sim' if plan.is_spring_boot_project else 'não'}")

    if plan.warnings:
        typer.echo("\nAvisos:")
        for warning in plan.warnings:
            typer.echo(f"- {warning}")

    if not plan.can_apply:
        raise typer.Exit(code=1 if not plan.is_spring_boot_project else 0)

    typer.echo("\nAções planejadas:")
    for index, action in enumerate(plan.actions, start=1):
        typer.echo(f"{index}. {action.description} ({action.relative_path})")

    def confirm_action(action: SpringMvcAction) -> bool:
        typer.echo(f"\nPróxima ação: {action.description}")
        typer.echo(f"Destino: {action.relative_path}")
        try:
            return typer.confirm("Executar esta ação?", default=False)
        except typer.Abort:
            typer.echo("Entrada encerrada; ação negada para manter o usuário no controle.")
            return False

    _, results = workflow.execute(project_path, confirm_action)

    typer.echo("\nResultado:")
    for result in results:
        marker = "✅" if result.status == "created" else "↩"
        typer.echo(f"{marker} {result.action.relative_path}: {result.message}")


if __name__ == "__main__":
    app()
