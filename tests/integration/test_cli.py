from typer.testing import CliRunner

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Stack Base" in result.stdout
    assert "0.1.0" in result.stdout


def test_create_command() -> None:
    result = runner.invoke(app, ["create", "meu-projeto"])

    assert result.exit_code == 0
    assert "meu-projeto" in result.stdout