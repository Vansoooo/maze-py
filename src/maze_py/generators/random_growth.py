"""Randomized growth (growing tree) maze generator."""

from __future__ import annotations

import random
from typing import List, Tuple

from ..animation import AnimationRecorder
from ..grid import Cell, MazeGrid, MazeTree
from .base import MazeGenerator


class RandomGrowthGenerator(MazeGenerator):
    """Implements a growing tree variant with random cell selection."""

    def __init__(self, *, seed: int | None = None):
        self._random = random.Random(seed)

    def generate(
        self,
        grid: MazeGrid,
        start: Tuple[int, int],
        *,
        recorder: AnimationRecorder | None = None,
    ) -> MazeTree:
        grid.reset()
        root = grid.cell(*start)
        visit_order: List[Cell] = []

        active: List[Cell] = [root]
        visited = {root.coords}
        step = 0

        while active:
            idx = self._random.randrange(len(active))
            cell = active[idx]
            visit_order.append(cell)
            if recorder:
                recorder.record(
                    "generate",
                    "activate",
                    cell=list(cell.coords),
                    step=step,
                )
            step += 1

            candidates = [
                neighbor
                for neighbor in grid.neighbors(cell)
                if neighbor.coords not in visited
            ]

            if not candidates:
                active.pop(idx)
                continue

            neighbor = self._random.choice(candidates)
            visited.add(neighbor.coords)
            grid.link(cell, neighbor)
            neighbor.parent = cell
            cell.children.append(neighbor)
            active.append(neighbor)
            if recorder:
                recorder.record(
                    "generate",
                    "link",
                    parent=list(cell.coords),
                    child=list(neighbor.coords),
                )

        return MazeTree(grid=grid, root=root, visit_order=visit_order)

