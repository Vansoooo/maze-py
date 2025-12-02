"""Base interfaces for maze generators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from ..animation import AnimationRecorder
from ..grid import MazeGrid, MazeTree


class MazeGenerator(ABC):
    """Interface for classes that carve passages in a grid."""

    @abstractmethod
    def generate(
        self,
        grid: MazeGrid,
        start: Tuple[int, int],
        *,
        recorder: AnimationRecorder | None = None,
    ) -> MazeTree:
        """Return a full spanning tree rooted at ``start``."""

