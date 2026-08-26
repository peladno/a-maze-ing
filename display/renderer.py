from abc import ABC, abstractmethod
from typing import Protocol


class MazeLike(Protocol):
    """Minimum maze interface required by a renderer."""

    width: int
    height: int

    def walls_at(self, pos: tuple[int, int]) -> int:
        """Return the wall bitmask for the cell at ``(x, y)``."""
        ...


class Renderer(ABC):
    """Common interface implemented by maze renderers."""

    @abstractmethod
    def render(self, maze: MazeLike) -> None:
        """Render ``maze`` to the renderer's output target."""
        raise NotImplementedError
