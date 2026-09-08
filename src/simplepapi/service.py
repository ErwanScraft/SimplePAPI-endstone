from __future__ import annotations

import re
from typing import TYPE_CHECKING

from endstone import Player
from endstone.plugin import Service

from .expansion import PlaceholderExpansion

if TYPE_CHECKING:
    from endstone.plugin import Plugin


class SimplePAPIService(Service):
    """Core service responsible for registering and resolving placeholders."""

    SERVICE_NAME = "simplepapi"

    _PLACEHOLDER_PATTERN = re.compile(
        r"%([a-zA-Z0-9]+)_([a-zA-Z0-9_]+)%"
    )
    _IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9]+$")

    def __init__(self) -> None:
        super().__init__()

        self._expansions: dict[str, PlaceholderExpansion] = {}
        self._owners: dict[str, Plugin] = {}
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    @property
    def expansions(self) -> tuple[PlaceholderExpansion, ...]:
        return tuple(self._expansions.values())

    @property
    def registered_identifiers(self) -> tuple[str, ...]:
        return tuple(sorted(self._expansions))

    def register_expansion(
        self,
        plugin: Plugin,
        expansion: PlaceholderExpansion,
    ) -> None:
        identifier = expansion.identifier.strip().lower()

        if not identifier:
            raise ValueError("Expansion identifier cannot be empty.")

        if not self._IDENTIFIER_PATTERN.fullmatch(identifier):
            raise ValueError(
                f"Invalid expansion identifier: {identifier!r}"
            )

        if identifier in self._expansions:
            raise ValueError(
                f"Expansion already registered: {identifier!r}"
            )

        self._expansions[identifier] = expansion
        self._owners[identifier] = plugin

    def unregister_expansion(self, identifier: str) -> bool:
        identifier = identifier.strip().lower()

        if identifier not in self._expansions:
            return False

        del self._expansions[identifier]
        del self._owners[identifier]

        return True

    def unregister_expansions(self, plugin: Plugin) -> None:
        identifiers = [
            identifier
            for identifier, owner in self._owners.items()
            if owner is plugin
        ]

        for identifier in identifiers:
            self.unregister_expansion(identifier)

    def set_placeholders(
        self,
        player: Player | None,
        text: str,
    ) -> str:
        """Replace all registered placeholders in the given text."""

        if not self._active or not text:
            return text

        return self._PLACEHOLDER_PATTERN.sub(
            lambda match: self._resolve_match(player, match),
            text,
        )

    def _resolve_match(
        self,
        player: Player | None,
        match: re.Match[str],
    ) -> str:
        identifier = match.group(1).lower()
        params = match.group(2).lower()

        expansion = self._expansions.get(identifier)

        if expansion is None:
            return match.group(0)

        value = expansion.on_request(player, params)

        if value is None:
            return match.group(0)

        return str(value)

    def activate(self) -> None:
        self._active = True

    def deactivate(self) -> None:
        self._active = False
        self._expansions.clear()
        self._owners.clear()