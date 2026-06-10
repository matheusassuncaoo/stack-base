import tempfile
import unittest
from pathlib import Path

from app.generator import ProjectGenerator
from app.models.project_config import ProjectConfig


class TestProjectGenerator(unittest.TestCase):
    def test_generates_python_fastapi_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            config = ProjectConfig(
                name="demo-api",
                stack="Python + FastAPI",
                architecture="MVC",
                database="Sem banco de dados",
                output_directory=Path(temporary_directory),
                use_docker=True,
                use_tests=True,
                use_ci=True,
            )

            project_path = ProjectGenerator().generate(config)

            self.assertTrue((project_path / "README.md").is_file())
            self.assertTrue((project_path / "project-config.yaml").is_file())
            self.assertTrue((project_path / "Dockerfile").is_file())
            self.assertTrue((project_path / ".github/workflows/build.yml").is_file())
            self.assertTrue((project_path / "src/demo_api/main.py").is_file())
            self.assertTrue((project_path / "tests/test_health.py").is_file())


if __name__ == "__main__":
    unittest.main()
