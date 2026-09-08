from __future__ import annotations

from endstone.plugin import Plugin, ServicePriority

from .expansions import PlayerExpansion, ServerExpansion
from .service import PlaceholderAPI


class SimplePAPIPlugin(Plugin):
    api_version = "0.11"

    def __init__(self) -> None:
        super().__init__()
        self._service = PlaceholderAPI()

    def on_enable(self) -> None:
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

        self._service.activate()

        self.logger.info(
            "SimplePAPI enabled with %d expansions.",
            len(self._service.registered_identifiers),
        )

    def on_disable(self) -> None:
        self._service.deactivate()

        self.server.service_manager.unregister_all(self)