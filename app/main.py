import typer

from app.ui.application import run

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


if __name__ == "__main__":
    app()
