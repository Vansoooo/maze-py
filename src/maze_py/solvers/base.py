"""Base interfaces for maze solvers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from time import perf_counter
from typing import Dict, List, Tuple

from ..animation import AnimationRecorder
from ..grid import Cell, MazeTree
from .results import MazeSolution, SolverStats


class MazeSolver(ABC):
    """Interface for path-finding within a maze tree."""

    name: str = "solver"

    def solve(
        self,
        tree: MazeTree,
        target: Tuple[int, int],
        *,
        recorder: AnimationRecorder | None = None,
    ) -> MazeSolution:
        start = perf_counter()
        path, explored = self._traverse(tree, target, recorder=recorder)
        runtime_ms = (perf_counter() - start) * 1000
        stats = SolverStats(
            algorithm=self.name,
            nodes_expanded=len(explored),
            path_length=len(path) - 1 if path else 0,
            runtime_ms=runtime_ms,
        )
        return MazeSolution(
            path=path,
            explored=explored,
            found=bool(path),
            stats=stats,
        )

    @abstractmethod
    def _traverse(
        self,
        tree: MazeTree,
        target: Tuple[int, int],
        *,
        recorder: AnimationRecorder | None = None,
    ) -> Tuple[List[Cell], List[Cell]]:
        """Return the visited order and final path."""

    def _build_path(
        self,
        parents: Dict[Cell, Cell | None],
        target: Cell,
    ) -> List[Cell]:
        if target not in parents:
            return []
        cursor: Cell | None = target
        path: List[Cell] = []
        while cursor is not None:
            path.append(cursor)
            cursor = parents[cursor]
        return list(reversed(path))

