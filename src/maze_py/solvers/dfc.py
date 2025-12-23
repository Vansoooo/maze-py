from __future__ import annotations 
from typing import List, Dict, Tuple
from ..animation import AnimationRecorder
from ..grid import Cell, MazeTree
from .base import MazeSolver

class DepthFirstSolver(MazeSolver):
    
    name = "dfs"

    def _traverse(
        self,
        tree: MazeTree,
        target: Tuple[int, int],
        *,
        recorder: AnimationRecorder | None = None,
    ) -> Tuple[List[Cell], List[Cell]]:
        target_cell = tree.grid.cell(*target)
        stack: List[Cell] = [tree.root]
        parents: Dict[Cell, Cell | None] = {tree.root: None}
        explored: List[Cell] = []
        while stack:
            cell = stack.pop()
            
            explored.append(cell)
            
            if recorder:
                recorder.record(
                    "solve",
                    "explore",
                    cell=list(cell.coords),
                    parent=list(parents[cell].coords) if parents[cell] else None,
                )
            if cell is target_cell:
                break
            for neighbor in cell.links:
                if neighbor in parents:
                    continue
                
                parents[neighbor] = cell
                stack.append(neighbor)
        path = self._build_path(parents, target_cell)

        if path and recorder:
            recorder.record(
                "solve",
                "path",
                cells=[list(step.coords) for step in path],
            )
        return path, explored
