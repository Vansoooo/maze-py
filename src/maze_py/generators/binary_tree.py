"""Binary tree maze generator."""

from __future__ import annotations

import random
from typing import List, Tuple

from ..animation import AnimationRecorder
from ..grid import Cell, MazeGrid, MazeTree
from .base import MazeGenerator


class BinaryTreeGenerator(MazeGenerator):
    """Carves passages by linking each cell east or south."""

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
        visit_order: List[Cell] = []
        root = grid.cell(*start)

        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.cell(x, y)
                visit_order.append(cell)
                if recorder:
                    recorder.record(
                        "generate",
                        "activate",
                        cell=[x, y],
                        step=len(visit_order),
                    )
                choices = []
                if grid.contains(x + 1, y):
                    choices.append(grid.cell(x + 1, y))
                if grid.contains(x, y + 1):
                    choices.append(grid.cell(x, y + 1))
                if not choices:
                    continue
                neighbor = self._random.choice(choices)
                grid.link(cell, neighbor)
                neighbor.parent = cell
                cell.children.append(neighbor)
                if recorder:
                    recorder.record(
                        "generate",
                        "link",
                        parent=[cell.x, cell.y],
                        child=[neighbor.x, neighbor.y],
                    )

        return MazeTree(grid=grid, root=root, visit_order=visit_order)

