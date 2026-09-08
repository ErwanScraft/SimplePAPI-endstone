from __future__ import annotations

from endstone import Player

from ..expansion import PlaceholderExpansion


STONEPERMS_SERVICE = "stoneperms.permissions.v1"


class StonePermsExpansion(PlaceholderExpansion):
    identifier = "stoneperms"
    author = "ErwanScraft"
    version = "1.0.0"

    def __init__(self, server) -> None:
        self._server = server

    def on_request(
        self,
        player: Player | None,
        params: str,
    ) -> str | None:
        if player is None:
            return None

        service = self._server.service_manager.load(
            STONEPERMS_SERVICE
        )

        if service is None:
            return None

        parameter = params.strip()

        if not parameter:
            return None

        if parameter == "primary_group":
            return service.get_primary_group(player)

        if parameter == "groups":
            return ", ".join(
                service.get_groups(player)
            )

        if parameter == "prefix":
            return service.get_prefix(player) or ""

        if parameter == "suffix":
            return service.get_suffix(player) or ""

        if parameter == "tracks":
            return self._format_tracks(
                service.get_user_tracks(player)
            )

        if parameter.startswith("meta_"):
            key = parameter[len("meta_") :]

            if not key:
                return None

            return service.get_meta(
                player,
                key,
            ) or ""

        if parameter.startswith("permission_"):
            permission = parameter[len("permission_") :]

            if not permission:
                return None

            decision = service.check_permission(
                player,
                permission,
            )

            return decision.value

        if parameter.startswith("has_permission_"):
            permission = parameter[
                len("has_permission_") :
            ]

            if not permission:
                return None

            return str(
                service.has_permission(
                    player,
                    permission,
                )
            ).lower()

        if parameter.startswith("track_"):
            track_name = parameter[len("track_") :]

            if not track_name:
                return None

            tracks = service.get_user_tracks(player)

            groups = tracks.get(track_name)

            if groups is None:
                return None

            return ", ".join(groups)

        return None

    @staticmethod
    def _format_tracks(
        tracks: dict[str, tuple[str, ...]],
    ) -> str:
        return ", ".join(
            f"{name}: {', '.join(groups)}"
            for name, groups in tracks.items()
        )