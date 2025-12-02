"""Solution dataclasses for maze solvers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..grid import Cell


@dataclass(slots=True)
class SolverStats:
    algorithm: str
    nodes_expanded: int
    path_length: int
    runtime_ms: float


@dataclass(slots=True)
class MazeSolution:
    path: List[Cell]
    explored: List[Cell]
    found: bool
    stats: SolverStats

    @property
    def steps(self) -> int:
        return self.stats.path_length

