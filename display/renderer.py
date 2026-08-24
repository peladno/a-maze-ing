from typing import Any, Protocol


class Renderer(Protocol):
    def render(self, maze: Any) -> None:  # Change Maze type when is available
        raise NotImplementedError
