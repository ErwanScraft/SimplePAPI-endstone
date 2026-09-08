from __future__ import annotations

import re
from typing import TYPE_CHECKING

from endstone import Player
from endstone.plugin import Service

from .expansion import PlaceholderExpansion

if TYPE_CHECKING:
    from endstone.plugin import Plugin


class PlaceholderAPI(Service):
    """Core PlaceholderAPI service."""

    SERVICE_NAME = "simplepapi"

    _PLACEHOLDER_PATTERN = re.compile(
        r"%([a-zA-Z0-9_]+)(?:_([a-zA-Z0-9_]+))?%"
    )

    def __init__(self) -> None:
        super().__init__()
        self._expansions: dict[str, PlaceholderExpansion] = {}
        self._owners: dict[str, Plugin] = {}
        self.active = False

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
    ) -> bool:
        identifier = expansion.identifier.strip().lower()

        if not identifier:
            raise ValueError("Expansion identifier cannot be empty.")

        if identifier in self._expansions:
            return False

        self._expansions[identifier] = expansion
        self._owners[identifier] = plugin

        return True

    def unregister_expansion(
        self,
        identifier: str,
    ) -> bool:
        identifier = identifier.lower()

        if identifier not in self._expansions:
            return False

        self._expansions.pop(identifier)
        self._owners.pop(identifier, None)

        return True

    def unregister_expansions(
        self,
        plugin: Plugin,
    ) -> None:
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
        if not text or not self.active:
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
        params = match.group(2) or ""

        expansion = self._expansions.get(identifier)

        if expansion is None:
            return match.group(0)

        try:
            value = expansion.on_request(player, params)
        except Exception:
            return match.group(0)

        if value is None:
            return match.group(0)

        return str(value)

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False
        self._expansions.clear()
        self._owners.clear()