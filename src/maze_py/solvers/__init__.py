"""Solver exports."""

from .breadth_first import BreadthFirstSolver
# from .depth_first import DepthFirstSolver
# from .dijkstra import DijkstraSolver
from .results import MazeSolution, SolverStats

__all__ = [
    "BreadthFirstSolver",
     "DepthFirstSolver",
    # "DijkstraSolver",
    "MazeSolution",
    "SolverStats",
]

