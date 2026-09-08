from __future__ import annotations

from endstone import Player, Server

from ..expansion import PlaceholderExpansion


class ServerExpansion(PlaceholderExpansion):
    """Provides server-related placeholders."""

    identifier = "server"
    author = "ErwanScraft"
    version = "1.0.0"

    def __init__(self, server: Server) -> None:
        self._server = server

    def on_request(
        self,
        player: Player | None,
        params: str,
    ) -> str | None:
        if params == "online":
            return str(len(self._server.online_players))

        if params == "max_players":
            return str(self._server.max_players)

        return None