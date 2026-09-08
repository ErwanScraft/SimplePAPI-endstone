from __future__ import annotations

from endstone import Player

from ..expansion import PlaceholderExpansion


class PlayerExpansion(PlaceholderExpansion):
    """Provides player-related placeholders."""

    identifier = "player"
    author = "ErwanScraft"
    version = "1.0.0"

    def on_request(
        self,
        player: Player | None,
        params: str,
    ) -> str | None:
        if player is None:
            return None

        if params == "name":
            return player.name

        if params == "uuid":
            return str(player.unique_id)

        if params == "ping":
            return str(player.ping)

        return None