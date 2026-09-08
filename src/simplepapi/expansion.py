from __future__ import annotations

from abc import ABC, abstractmethod

from endstone import Player


class PlaceholderExpansion(ABC):
    """Base class for a SimplePAPI placeholder expansion."""

    identifier: str = ""
    author: str = ""
    version: str = "1.0.0"

    @abstractmethod
    def on_request(
        self,
        player: Player | None,
        params: str,
    ) -> str | None:
        """Resolve a placeholder request."""
        raise NotImplementedError