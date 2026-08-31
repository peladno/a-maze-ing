"""Abstract interfaces and protocols for maze renderers."""

from abc import ABC, abstractmethod
from typing import Protocol


class MazeLike(Protocol):
    """Minimum maze interface required by a renderer."""

    @property
    def width(self) -> int:
        """Return the grid width in cells."""
        ...

    @property
    def height(self) -> int:
        """Return the grid height in cells."""
        ...

    def walls_at(self, pos: tuple[int, int]) -> int:
        """Return the wall bitmask for the cell at ``(x, y)``."""
        ...


class Renderer(ABC):
    """Common interface implemented by maze renderers."""

    @abstractmethod
    def render(self, maze: MazeLike) -> None:
        """Render ``maze`` to the renderer's output target."""
        raise NotImplementedError
