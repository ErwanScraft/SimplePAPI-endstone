from __future__ import annotations

from endstone.plugin import Plugin, ServicePriority

from .expansions import (
    PlayerExpansion,
    ServerExpansion,
    StonePermsExpansion,
)
from .service import SimplePAPIService


class SimplePAPIPlugin(Plugin):
    """SimplePAPI Endstone plugin."""

    api_version = "0.11"
    soft_depend = ["stoneperms"]

    def __init__(self) -> None:
        super().__init__()

        self._service = SimplePAPIService()

    def on_enable(self) -> None:
        service_manager = self.server.service_manager

        self.server.service_manager.register(
            PlaceholderAPI.SERVICE_NAME,
            self._service,
            self,
            ServicePriority.NORMAL,
        )
        
        self._service.register_expansion(
            self,
            PlayerExpansion(),
        )
        
        self._service.register_expansion(
            self,
            ServerExpansion(self.server),
        )
        
        self._service.register_expansion(
            self,
            StonePermsExpansion(self.server),
        )
        
        self._service.activate()

        self.logger.info(
            f"SimplePAPI enabled with "
            f"{len(self._service.expansions)} expansions."
        )

    def on_disable(self) -> None:
        self._service.deactivate()
        self.server.service_manager.unregister_all(self)

    def _register_expansions(self) -> None:
        self._service.register_expansion(
            self,
            PlayerExpansion(),
        )

        self._service.register_expansion(
            self,
            ServerExpansion(self.server),
        )