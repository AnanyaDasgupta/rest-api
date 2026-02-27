from pathlib import Path


def normalize_database_url(database_url: str, base_dir: Path) -> str:
    """Normalize relative SQLite URLs so app and migrations use the same DB file.

    `sqlite:///students.db` is a relative path that depends on process working
    directory. We resolve it against `base_dir` to avoid runtime/migration drift
    when commands are launched from different directories.
    """

    sqlite_relative_prefix = "sqlite:///"

    if not database_url.startswith(sqlite_relative_prefix):
        return database_url

    sqlite_path = database_url[len(sqlite_relative_prefix) :]

    # Keep special SQLite URLs unchanged.
    if sqlite_path in {":memory:", ""}:
        return database_url

    path_obj = Path(sqlite_path)
    if path_obj.is_absolute():
        return database_url

    resolved_path = (base_dir / path_obj).resolve()
    return f"sqlite:///{resolved_path}"

