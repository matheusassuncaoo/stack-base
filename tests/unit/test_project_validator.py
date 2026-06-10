import tempfile
import unittest
from pathlib import Path

from app.validation.project_detector import ProjectDetector


class TestProjectDetector(unittest.TestCase):
    def test_detects_java_spring_maven_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root_path = Path(temporary_directory)

            source_path = root_path / "src/main/java/com/example"
            source_path.mkdir(parents=True)

            pom_content = """
            <project>
                <dependencies>
                    <dependency>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-starter-web</artifactId>
                    </dependency>

                    <dependency>
                        <groupId>org.springframework.boot</groupId>
                        <artifactId>spring-boot-starter-data-jpa</artifactId>
                    </dependency>

                    <dependency>
                        <groupId>com.oracle.database.jdbc</groupId>
                        <artifactId>ojdbc11</artifactId>
                    </dependency>
                </dependencies>
            </project>
            """

            (root_path / "pom.xml").write_text(
                pom_content,
                encoding="utf-8",
            )

            (source_path / "Application.java").write_text(
                """
                @SpringBootApplication
                public class Application {
                }
                """,
                encoding="utf-8",
            )

            detector = ProjectDetector()
            result = detector.detect(root_path)

            self.assertTrue(result.is_valid_project)

            self.assertTrue(
                any(
                    technology.name == "Java"
                    for technology in result.languages
                )
            )

            self.assertTrue(
                any(
                    technology.name == "Spring Boot"
                    for technology in result.frameworks
                )
            )

            self.assertTrue(
                any(
                    technology.name == "Maven"
                    for technology in result.build_tools
                )
            )

            self.assertTrue(
                any(
                    technology.name == "SQL"
                    for technology in result.capabilities
                )
            )

            self.assertTrue(
                any(
                    technology.name == "oracle"
                    for technology in result.providers
                )
            )


if __name__ == "__main__":
    unittest.main()