"""Helpers for writing animation data to disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from .animation import AnimationRecorder
from .grid import MazeGrid, MazeTree
from .solvers.results import MazeSolution


def write_animation_package(
    destination: str | Path,
    grid: MazeGrid,
    tree: MazeTree,
    solution: MazeSolution,
    recorder: AnimationRecorder,
    *,
    start: Tuple[int, int],
    target: Tuple[int, int],
) -> Path:
    """Serialize the run metadata and event stream into a JSON file."""

    payload = {
        "grid": {"width": grid.width, "height": grid.height},
        "start": list(start),
        "target": list(target),
        "found": solution.found,
        "events": recorder.to_serializable(),
    }
    destination_path = Path(destination).expanduser().resolve()
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return destination_path

