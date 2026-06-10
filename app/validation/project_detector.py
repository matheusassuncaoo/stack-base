from pathlib import Path

from app.infrastructure.project_reader import ProjectReader
from app.models.detected_project import (
    DetectedProject,
    Technology,
)
from app.validation.detection_rules import (
    DATABASE_PROVIDERS,
    NOSQL_DEPENDENCIES,
    SPRING_DEPENDENCIES,
    SQL_DEPENDENCIES,
    TEST_DEPENDENCIES,
)


class ProjectDetector:
    """Detecta as tecnologias existentes em um projeto."""

    def __init__(
        self,
        reader: ProjectReader | None = None,
    ) -> None:
        self.reader = reader or ProjectReader()

    def detect(
        self,
        project_path: str | Path,
    ) -> DetectedProject:
        root_path = Path(project_path).expanduser().resolve()

        result = DetectedProject(
            root_path=root_path,
            name=root_path.name,
        )

        if not root_path.exists():
            result.warnings.append(
                "O diretório informado não existe."
            )
            return result

        if not root_path.is_dir():
            result.warnings.append(
                "O caminho informado não é um diretório."
            )
            return result

        build_content = self._read_build_file(
            root_path,
            result,
        )

        self._detect_java(root_path, build_content, result)
        self._detect_spring(root_path, build_content, result)
        self._detect_persistence(build_content, result)
        self._detect_database_provider(build_content, result)
        self._detect_docker(root_path, result)
        self._detect_tests(root_path, build_content, result)

        result.is_valid_project = bool(
            result.languages
            or result.frameworks
            or result.build_tools
        )

        if not result.is_valid_project:
            result.warnings.append(
                "Nenhuma tecnologia conhecida foi detectada."
            )

        return result

    def _read_build_file(
        self,
        root_path: Path,
        result: DetectedProject,
    ) -> str:
        build_files = [
            "pom.xml",
            "build.gradle",
            "build.gradle.kts",
        ]

        contents: list[str] = []

        for build_file in build_files:
            if self.reader.is_file(root_path, build_file):
                result.detected_files.append(build_file)
                contents.append(
                    self.reader.read_text(
                        root_path,
                        build_file,
                    )
                )

        return "\n".join(contents).lower()

    def _detect_java(
        self,
        root_path: Path,
        build_content: str,
        result: DetectedProject,
    ) -> None:
        has_java_directory = self.reader.is_directory(
            root_path,
            "src/main/java",
        )

        has_java_files = bool(
            self.reader.find_files(root_path, "*.java")
        )

        if has_java_directory or has_java_files:
            result.languages.append(
                Technology(
                    category="language",
                    name="Java",
                    confidence=1.0,
                )
            )

        if self.reader.is_file(root_path, "pom.xml"):
            result.build_tools.append(
                Technology(
                    category="build-tool",
                    name="Maven",
                    confidence=1.0,
                )
            )

        if (
            self.reader.is_file(root_path, "build.gradle")
            or self.reader.is_file(
                root_path,
                "build.gradle.kts",
            )
        ):
            result.build_tools.append(
                Technology(
                    category="build-tool",
                    name="Gradle",
                    confidence=1.0,
                )
            )

    def _detect_spring(
        self,
        root_path: Path,
        build_content: str,
        result: DetectedProject,
    ) -> None:
        has_dependency = any(
            dependency in build_content
            for dependency in SPRING_DEPENDENCIES
        )

        java_files = self.reader.find_files(
            root_path,
            "*.java",
        )

        has_annotation = any(
            "@springbootapplication"
            in file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()
            for file_path in java_files
        )

        if has_dependency or has_annotation:
            result.frameworks.append(
                Technology(
                    category="framework",
                    name="Spring Boot",
                    confidence=(
                        1.0
                        if has_dependency and has_annotation
                        else 0.85
                    ),
                )
            )

    @staticmethod
    def _detect_persistence(
        build_content: str,
        result: DetectedProject,
    ) -> None:
        if any(
            dependency in build_content
            for dependency in SQL_DEPENDENCIES
        ):
            result.capabilities.append(
                Technology(
                    category="persistence",
                    name="SQL",
                )
            )

        if any(
            dependency in build_content
            for dependency in NOSQL_DEPENDENCIES
        ):
            result.capabilities.append(
                Technology(
                    category="persistence",
                    name="NoSQL",
                )
            )

    @staticmethod
    def _detect_database_provider(
        build_content: str,
        result: DetectedProject,
    ) -> None:
        for provider, indicators in DATABASE_PROVIDERS.items():
            if any(
                indicator in build_content
                for indicator in indicators
            ):
                result.providers.append(
                    Technology(
                        category="database-provider",
                        name=provider,
                        confidence=0.95,
                    )
                )

    def _detect_docker(
        self,
        root_path: Path,
        result: DetectedProject,
    ) -> None:
        docker_files = [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
            "compose.yml",
            "compose.yaml",
        ]

        if any(
            self.reader.is_file(root_path, file_name)
            for file_name in docker_files
        ):
            result.capabilities.append(
                Technology(
                    category="container",
                    name="Docker",
                )
            )

    def _detect_tests(
        self,
        root_path: Path,
        build_content: str,
        result: DetectedProject,
    ) -> None:
        has_test_directory = self.reader.is_directory(
            root_path,
            "src/test",
        )

        has_test_dependency = any(
            dependency in build_content
            for dependency in TEST_DEPENDENCIES
        )

        if has_test_directory or has_test_dependency:
            result.capabilities.append(
                Technology(
                    category="testing",
                    name="Tests",
                    confidence=(
                        1.0
                        if has_test_directory
                        and has_test_dependency
                        else 0.8
                    ),
                )
            )