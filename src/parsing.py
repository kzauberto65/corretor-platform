from pathlib import Path

def get_project_root():
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "src").exists() and (parent / "database").exists():
            return parent

    return current.parents[1]