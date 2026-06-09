import typer
from rich.console import Console

console = Console()

app = typer.Typer(
    name="stackbase",
    help="Gera, padroniza e valida projetos de software.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Exibe a versão atual do Stack Base."""
    console.print("[bold green]Stack Base[/bold green] versão 0.1.0")


@app.command()
def create(
    name: str = typer.Argument(
        ...,
        help="Nome do projeto que será criado.",
    ),
) -> None:
    """Cria um novo projeto."""
    console.print(f"[bold cyan]Criando projeto:[/bold cyan] {name}")