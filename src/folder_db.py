from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import sys


@dataclass(frozen=True)
class ProjectPaths:
    """Namespace for commonly used project folders."""

    root: Path
    data: Path
    raw_beh: Path
    parsed_beh: Path


@lru_cache(maxsize=1)
def get_project_paths(root: Path | None = None) -> ProjectPaths:
    """
    Return resolved paths for the project.

    If root is not provided, it is inferred from the location of this file.
    """
    base = Path(root).resolve() if root else Path(__file__).resolve().parent.parent
    data_dir = base / "data"
    return ProjectPaths(
        root=base,
        data=data_dir,
        raw_beh=data_dir / "raw" / "beh",
        parsed_beh=data_dir / "parsed" / "beh",
    )


# Ready-to-use namespace with default project root.
PATHS = get_project_paths()


def add_project_root_to_syspath(position: int = 0) -> Path:
    """
    Ensure the project root is on sys.path so imports work without hardcoding paths.

    Parameters
    ----------
    position : int
        Index to insert the project root in sys.path (defaults to the front).
    """
    root_str = str(PATHS.root)
    if root_str not in sys.path:
        insert_at = max(position, 0)
        sys.path.insert(insert_at, root_str)
    return PATHS.root


add_project_root_to_syspath()


def list_immediate_subdirs(path: Path) -> list[str]:
    return sorted(p.name for p in path.iterdir() if p.is_dir())


def main() -> None:
    sections = {
        "raw/beh": PATHS.raw_beh,
        "parsed/beh": PATHS.parsed_beh,
    }
    lines = []
    for label, path in sections.items():
        lines.append(f"[{label}]")
        for name in list_immediate_subdirs(path):
            lines.append(name)
        lines.append("")

    output = PATHS.root / "folder_database.txt"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
