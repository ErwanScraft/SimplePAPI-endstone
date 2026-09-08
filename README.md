Using SimplePAPI

SimplePAPI provides a lightweight and extensible placeholder service for Endstone plugins.

Other plugins can access the SimplePAPI service through Endstone's "ServiceManager".

Service Name

The registered service name is:

simplepapi

Accessing the Service

Retrieve the service from your plugin:

from endstone.plugin import Plugin

from simplepapi import SimplePAPIService


class MyPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self) -> None:
        service = self.server.service_manager.load(
            SimplePAPIService.SERVICE_NAME
        )

        if service is None:
            self.logger.warning(
                "SimplePAPI is not installed or unavailable."
            )
            return

        self.papi = service

Resolving Placeholders

Use "set_placeholders()" to replace placeholders in a string:

message = self.papi.set_placeholders(
    player,
    "Welcome %player_name%!"
)

For example:

Welcome Steve!

The player argument may be "None" when resolving server-only placeholders.

Available Placeholders

Player

Placeholder| Description
"%player_name%"| Player name
"%player_uuid%"| Player UUID
"%player_ping%"| Player ping

Player placeholders require a valid "Player" instance.

Server

Placeholder| Description
"%server_online%"| Current number of online players
"%server_max_players%"| Maximum number of players

Server placeholders can be resolved without a player.

Example

message = self.papi.set_placeholders(
    player,
    (
        "Player: %player_name%\n"
        "UUID: %player_uuid%\n"
        "Ping: %player_ping%ms\n"
        "Online: %server_online%/%server_max_players%"
    ),
)

Example result:

Player: Steve
UUID: 550e8400-e29b-41d4-a716-446655440000
Ping: 42ms
Online: 5/20

Unknown Placeholders

Unknown or unsupported placeholders are preserved.

message = self.papi.set_placeholders(
    player,
    "Hello %player_name% %unknown_placeholder%"
)

Result:

Hello Steve %unknown_placeholder%

This prevents unsupported placeholders from silently becoming empty strings.

Placeholder Case

Placeholder identifiers and parameters are case-insensitive.

These are equivalent:

%player_name%
%PLAYER_NAME%
%Player_Name%

Plugin Dependency

SimplePAPI is accessed as a runtime service rather than through direct coupling to its implementation.

Your plugin should gracefully handle the case where the service is unavailable:

service = self.server.service_manager.load("simplepapi")

if service is None:
    # SimplePAPI is unavailable.
    return

This allows your plugin to continue operating when SimplePAPI is not installed.

Creating Custom Expansions

SimplePAPI is designed to be extended through "PlaceholderExpansion".

Example:

from endstone import Player

from simplepapi import PlaceholderExpansion


class MyExpansion(PlaceholderExpansion):
    identifier = "myplugin"
    author = "MyPlugin"
    version = "1.0.0"

    def on_request(
        self,
        player: Player | None,
        params: str,
    ) -> str | None:
        if params == "example":
            return "Hello"

        return None

This expansion provides:

%myplugin_example%

Custom expansions should be registered with the SimplePAPI service by their owning plugin.

The expansion identifier must contain only letters and numbers:

myplugin
economy
jobs
clan

Parameters may contain underscores:

%myplugin_example%
%economy_balance_formatted%
%clan_member_count%