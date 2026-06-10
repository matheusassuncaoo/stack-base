from pathlib import Path

from app.models.project_config import ProjectConfig


class ProjectGenerationError(Exception):
    """Erro de validação ou escrita durante a geração do projeto."""


class ProjectGenerator:
    """Gera um projeto mínimo e expansível a partir da configuração da TUI."""

    def generate(self, config: ProjectConfig) -> Path:
        self._validate(config)

        project_path = config.project_path
        project_path.mkdir(parents=True, exist_ok=False)

        self._write_common_files(config, project_path)
        self._write_stack_files(config, project_path)

        if config.use_docker:
            self._write_docker_files(config, project_path)

        if config.use_ci:
            self._write_ci_files(config, project_path)

        return project_path

    @staticmethod
    def _validate(config: ProjectConfig) -> None:
        if not config.name.strip():
            raise ProjectGenerationError("Informe um nome para o projeto.")

        if any(separator in config.name for separator in ("/", "\\")):
            raise ProjectGenerationError("O nome do projeto não deve conter barras.")

        if config.project_path.exists():
            raise ProjectGenerationError(
                f"O diretório '{config.project_path}' já existe. Escolha outro nome ou saída."
            )

    @staticmethod
    def _write_common_files(config: ProjectConfig, project_path: Path) -> None:
        (project_path / "README.md").write_text(
            f"""# {config.name}

Projeto gerado pelo Stack Base.

## Stack

- Stack: {config.stack}
- Arquitetura: {config.architecture}
- Banco de dados: {config.database}
- Docker: {'sim' if config.use_docker else 'não'}
- Testes: {'sim' if config.use_tests else 'não'}
- CI/CD: {'sim' if config.use_ci else 'não'}

## Próximos passos

1. Revise a estrutura inicial.
2. Instale as dependências da stack selecionada.
3. Evolua os módulos de domínio, aplicação e infraestrutura.
""",
            encoding="utf-8",
        )

        (project_path / ".gitignore").write_text(
            """.env
.env.*
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
target/
build/
dist/
node_modules/
.idea/
.vscode/
""",
            encoding="utf-8",
        )

        (project_path / "project-config.yaml").write_text(
            f"""name: {config.name}
stack: {config.stack}
architecture: {config.architecture}
database: {config.database}
features:
  docker: {str(config.use_docker).lower()}
  tests: {str(config.use_tests).lower()}
  ci: {str(config.use_ci).lower()}
""",
            encoding="utf-8",
        )

    def _write_stack_files(self, config: ProjectConfig, project_path: Path) -> None:
        if config.stack == "Java + Spring Boot":
            self._write_java_spring(config, project_path)
            return

        if config.stack == "Python + FastAPI":
            self._write_python_fastapi(config, project_path)
            return

        self._write_node_nest(config, project_path)

    @staticmethod
    def _write_java_spring(config: ProjectConfig, project_path: Path) -> None:
        package_path = project_path / "src" / "main" / "java" / "com" / "example" / "app"
        package_path.mkdir(parents=True)
        (package_path / "Application.java").write_text(
            """package com.example.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
""",
            encoding="utf-8",
        )

        dependencies = """
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>"""

        if config.database != "Sem banco de dados":
            dependencies += """
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>"""

        if config.use_tests:
            dependencies += """
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>"""
            (project_path / "src" / "test" / "java" / "com" / "example" / "app").mkdir(
                parents=True
            )

        (project_path / "pom.xml").write_text(
            f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<project xmlns=\"http://maven.apache.org/POM/4.0.0\">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>{config.name}</artifactId>
    <version>0.1.0</version>
    <properties>
        <java.version>21</java.version>
        <spring-boot.version>3.3.0</spring-boot.version>
    </properties>
    <dependencies>{dependencies}
    </dependencies>
</project>
""",
            encoding="utf-8",
        )

    @staticmethod
    def _write_python_fastapi(config: ProjectConfig, project_path: Path) -> None:
        app_path = project_path / "src" / config.name.replace("-", "_")
        app_path.mkdir(parents=True)
        (app_path / "__init__.py").write_text("", encoding="utf-8")
        (app_path / "main.py").write_text(
            """from fastapi import FastAPI

app = FastAPI(title="Stack Base App")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
""",
            encoding="utf-8",
        )
        if config.use_tests:
            tests_path = project_path / "tests"
            tests_path.mkdir()
            (tests_path / "test_health.py").write_text(
                """def test_health_contract() -> None:
    assert {"status": "ok"}["status"] == "ok"
""",
                encoding="utf-8",
            )
        (project_path / "pyproject.toml").write_text(
            f"""[project]
name = "{config.name}"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi", "uvicorn"]
""",
            encoding="utf-8",
        )

    @staticmethod
    def _write_node_nest(config: ProjectConfig, project_path: Path) -> None:
        src_path = project_path / "src"
        src_path.mkdir()
        (src_path / "main.ts").write_text(
            """async function bootstrap(): Promise<void> {
  console.log('Stack Base NestJS starter');
}

void bootstrap();
""",
            encoding="utf-8",
        )
        if config.use_tests:
            tests_path = project_path / "test"
            tests_path.mkdir()
            (tests_path / "app.e2e-spec.ts").write_text(
                """describe('app', () => {
  it('starts with an MVP contract', () => {
    expect(true).toBe(true);
  });
});
""",
                encoding="utf-8",
            )
        (project_path / "package.json").write_text(
            f"""{{
  "name": "{config.name}",
  "version": "0.1.0",
  "scripts": {{
    "start": "nest start",
    "test": "jest"
  }},
  "dependencies": {{
    "@nestjs/common": "latest",
    "@nestjs/core": "latest"
  }}
}}
""",
            encoding="utf-8",
        )

    @staticmethod
    def _write_docker_files(config: ProjectConfig, project_path: Path) -> None:
        (project_path / "Dockerfile").write_text(
            """FROM alpine:3.20
WORKDIR /app
COPY . .
CMD ["sh", "-c", "echo Stack Base project ready && sleep 1"]
""",
            encoding="utf-8",
        )
        (project_path / "docker-compose.yml").write_text(
            f"""services:
  app:
    build: .
    container_name: {config.name}
""",
            encoding="utf-8",
        )

    @staticmethod
    def _write_ci_files(config: ProjectConfig, project_path: Path) -> None:
        workflow_path = project_path / ".github" / "workflows"
        workflow_path.mkdir(parents=True)
        (workflow_path / "build.yml").write_text(
            """name: build

on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate scaffold
        run: test -f README.md
""",
            encoding="utf-8",
        )
