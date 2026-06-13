import tempfile
import unittest
from pathlib import Path

from typer.testing import CliRunner

from app.main import app


class TestSpringMvcCli(unittest.TestCase):
    def test_spring_mvc_command_keeps_user_control_per_action(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)
            source_path = root_path / "src/main/java/com/example/demo"
            source_path.mkdir(parents=True)
            (root_path / "pom.xml").write_text(
                """
                <project>
                    <dependencies>
                        <dependency>
                            <groupId>org.springframework.boot</groupId>
                            <artifactId>spring-boot-starter-web</artifactId>
                        </dependency>
                    </dependencies>
                </project>
                """,
                encoding="utf-8",
            )
            (source_path / "DemoApplication.java").write_text(
                """
                package com.example.demo;

                import org.springframework.boot.autoconfigure.SpringBootApplication;

                @SpringBootApplication
                public class DemoApplication {
                }
                """,
                encoding="utf-8",
            )

            result = CliRunner().invoke(app, ["spring-mvc", str(root_path)], input="n\n")

            self.assertEqual(result.exit_code, 0)
            self.assertIn("Executar esta ação?", result.output)
            self.assertIn("Ação recusada pelo usuário", result.output)
            self.assertFalse((root_path / "src/main/java/com/example/demo/controller").exists())


if __name__ == "__main__":
    unittest.main()
