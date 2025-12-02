"""Randomized spanning-tree maze generator."""

from __future__ import annotations

import random
from typing import List, Tuple

from ..animation import AnimationRecorder
from ..grid import Cell, MazeGrid, MazeTree
from .base import MazeGenerator


class SpanningTreeGenerator(MazeGenerator):
    """Generates a uniform spanning tree using a Prim-like frontier."""

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
        root.parent = None
        visit_order: List[Cell] = []

        frontier: List[Cell] = [root]
        visited = {root.coords}

        step = 0
        while frontier:
            idx = self._random.randrange(len(frontier))
            cell = frontier.pop(idx)
            visit_order.append(cell)
            if recorder:
                recorder.record(
                    "generate",
                    "activate",
                    cell=list(cell.coords),
                    step=step,
                )
            step += 1

            for neighbor in grid.neighbors(cell):
                if neighbor.coords in visited:
                    continue
                visited.add(neighbor.coords)
                grid.link(cell, neighbor)
                neighbor.parent = cell
                cell.children.append(neighbor)
                frontier.append(neighbor)
                if recorder:
                    recorder.record(
                        "generate",
                        "link",
                        parent=list(cell.coords),
                        child=list(neighbor.coords),
                    )

        return MazeTree(grid=grid, root=root, visit_order=visit_order)

