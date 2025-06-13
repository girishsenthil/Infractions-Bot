from pathlib import Path
from functools import lru_cache

@lru_cache()
def _find_project_root():
    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        # Look for a known anchor like .git or pyproject.toml
        if (parent / 'src').is_dir():
            return parent
    raise RuntimeError("Could not find project root")

PROJECT_ROOT = _find_project_root()

DB_FILE = PROJECT_ROOT / 'infractions.db'
SQL_DIR = PROJECT_ROOT / 'src' / 'sql'

__all__ = ['PROJECT_ROOT', 'DB_FILE', 'SQL_DIR']

