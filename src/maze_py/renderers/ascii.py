"""ASCII renderer for maze trees."""

from __future__ import annotations

from typing import Iterable

from ..grid import Cell, MazeTree
from ..solvers.results import MazeSolution


class AsciiRenderer:
    """Render mazes as monospaced strings."""

    def render(
        self,
        tree: MazeTree,
        solution: MazeSolution | None = None,
        *,
        start_token: str = "S",
        target_token: str = "T",
    ) -> str:
        width = tree.grid.width * 2 + 1
        height = tree.grid.height * 2 + 1
        canvas = [["#"] * width for _ in range(height)]

        def carve(cell: Cell) -> None:
            row = cell.y * 2 + 1
            col = cell.x * 2 + 1
            canvas[row][col] = " "
            for neighbor in cell.links:
                mid_row = cell.y + neighbor.y + 1
                mid_col = cell.x + neighbor.x + 1
                canvas[mid_row][mid_col] = " "

        for cell in tree.grid:
            carve(cell)

        if solution and solution.path:
            self._mark_path(canvas, solution.path, token="*")

        start_row = tree.root.y * 2 + 1
        start_col = tree.root.x * 2 + 1
        canvas[start_row][start_col] = start_token

        if solution and solution.path:
            target_cell = solution.path[-1]
            row = target_cell.y * 2 + 1
            col = target_cell.x * 2 + 1
            canvas[row][col] = target_token

        return "\n".join("".join(row) for row in canvas)

    def _mark_path(self, canvas: list[list[str]], path: Iterable[Cell], token: str) -> None:
        prev: Cell | None = None
        for cell in path:
            row = cell.y * 2 + 1
            col = cell.x * 2 + 1
            canvas[row][col] = token
            if prev:
                mid_row = cell.y + prev.y + 1
                mid_col = cell.x + prev.x + 1
                canvas[mid_row][mid_col] = token
            prev = cell

