from __future__ import annotations

"""Batch parser for PsychoPy log files that saves CSV outputs in bulk."""

import argparse
import sys
from pathlib import Path
from typing import Dict, List

try:
    from ..folder_db import PATHS
except ImportError:  # Fallback when running as a standalone script
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from folder_db import PATHS

try:
    from . import parse_psychopy
except ImportError:  # Fallback when running as a standalone script
    import parse_psychopy

DEFAULT_INPUT_DIR = PATHS.raw_beh
DEFAULT_OUTPUT_DIR = PATHS.parsed_beh


def _target_csv_path(log_path: Path, output_dir: Path) -> Path:
    """Return the CSV path for a given log file."""
    name = log_path.name
    if name.endswith(".log.gz"):
        csv_name = name[: -len(".log.gz")] + ".csv"
    else:
        csv_name = log_path.stem + ".csv"
    return output_dir / csv_name

def batch_parse_logs(
    input_dir: Path | None = None,
    output_dir: Path | None = None,
    pattern: str = "*.log*",
    overwrite: bool = False,
    dry_run: bool = False,
) -> List[Dict[str, str]]:
    """
    Parse all matching log files under input_dir and write CSVs to output_dir.

    By default, uses folder_db.PATHS to pull the raw/parsed behavioral folders.
    Returns a list of result dicts with keys: log, csv, status, and optionally error/trials.
    """
    input_dir = Path(input_dir).resolve() if input_dir else DEFAULT_INPUT_DIR
    output_dir = Path(output_dir).resolve() if output_dir else DEFAULT_OUTPUT_DIR

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    log_paths = sorted({p for p in input_dir.rglob(pattern) if p.is_file()})
    results: List[Dict[str, str]] = []

    for log_path in log_paths:
        csv_path = _target_csv_path(log_path, output_dir)

        if csv_path.exists() and not overwrite:
            results.append(
                {
                    "log": str(log_path),
                    "csv": str(csv_path),
                    "status": "skipped",
                    "reason": "exists",
                }
            )
            continue

        if dry_run:
            results.append(
                {
                    "log": str(log_path),
                    "csv": str(csv_path),
                    "status": "dry-run",
                }
            )
            continue

        csv_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            trials = parse_psychopy.parse_time_interval_log(str(log_path))
            parse_psychopy.save_trials_to_csv(trials, str(csv_path))
            results.append(
                {
                    "log": str(log_path),
                    "csv": str(csv_path),
                    "status": "ok",
                    "trials": str(len(trials)),
                }
            )
        except Exception as exc:  # noqa: BLE001 - want to record any failure
            results.append(
                {
                    "log": str(log_path),
                    "csv": str(csv_path),
                    "status": "error",
                    "error": str(exc),
                }
            )

    return results


def _print_summary(results: List[Dict[str, str]]) -> None:
    ok = [r for r in results if r["status"] == "ok"]
    skipped = [r for r in results if r["status"] == "skipped"]
    dry = [r for r in results if r["status"] == "dry-run"]
    errors = [r for r in results if r["status"] == "error"]

    for group, label in (
        (ok, "written"),
        (skipped, "skipped"),
        (dry, "dry-run"),
        (errors, "errors"),
    ):
        if not group:
            continue
        print(f"{label}: {len(group)}")
        for item in group:
            msg = f"  {item['log']} -> {item['csv']}"
            if "trials" in item:
                msg += f" ({item['trials']} trials)"
            if "reason" in item:
                msg += f" [{item['reason']}]"
            if "error" in item:
                msg += f" [error: {item['error']}]"
            print(msg)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Batch parse PsychoPy .log or .log.gz files into CSVs."
    )
    parser.add_argument(
        "--input-dir",
        default=None,
        type=Path,
        help=f"Directory containing log files (searches recursively). Default: {DEFAULT_INPUT_DIR}",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        type=Path,
        help=f"Directory to write CSV outputs. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--pattern",
        default="*.log*",
        help="Glob pattern for log files (relative to input-dir).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Rewrite CSVs even if they already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be done without writing files.",
    )

    args = parser.parse_args(argv)

    results = batch_parse_logs(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        pattern=args.pattern,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )
    _print_summary(results)


if __name__ == "__main__":
    main(sys.argv[1:])
