from pathlib import Path

from app.db_url import normalize_database_url


def test_normalize_relative_sqlite_url_to_absolute_path():
    base_dir = Path('/tmp/project')
    normalized = normalize_database_url('sqlite:///students.db', base_dir)

    assert normalized == 'sqlite:////tmp/project/students.db'


def test_keep_absolute_and_non_sqlite_urls_unchanged():
    base_dir = Path('/tmp/project')

    assert normalize_database_url('sqlite:////var/data/students.db', base_dir) == 'sqlite:////var/data/students.db'
    assert normalize_database_url('postgresql+psycopg://user:pass@localhost:5432/students', base_dir) == 'postgresql+psycopg://user:pass@localhost:5432/students'
