from pathlib import Path


class ProjectReader:
    """Responsável por ler arquivos e diretórios de um projeto."""

    @staticmethod
    def exists(
        root_path: Path,
        relative_path: str,
    ) -> bool:
        return (root_path / relative_path).exists()

    @staticmethod
    def is_file(
        root_path: Path,
        relative_path: str,
    ) -> bool:
        return (root_path / relative_path).is_file()

    @staticmethod
    def is_directory(
        root_path: Path,
        relative_path: str,
    ) -> bool:
        return (root_path / relative_path).is_dir()

    @staticmethod
    def read_text(
        root_path: Path,
        relative_path: str,
    ) -> str:
        file_path = root_path / relative_path

        if not file_path.is_file():
            return ""

        try:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            return ""

    @staticmethod
    def find_files(
        root_path: Path,
        pattern: str,
    ) -> list[Path]:
        if not root_path.exists():
            return []

        try:
            return list(root_path.rglob(pattern))
        except OSError:
            return []