from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerSkin:
    discordId: str
    palette: str
    description: Optional[str]
    effect: Optional[str]


@dataclass
class DiceConfig:
    custom_colors: str
    palettes: dict[str, list[str]]
    player_skins: dict[str, PlayerSkin]
    default_palette: str

    def _get_default_palette(self) -> list[str]:
        return self.palettes[self.default_palette]

    def is_custom_colors(self) -> bool:
        return self.custom_colors == "true"

    def get_player_palette(self, user_id: str) -> list[str]:
        player_skin = self.player_skins.get(user_id, None)
        if player_skin is None or player_skin.palette not in self.palettes:
            return self._get_default_palette()

        return self.palettes[player_skin.palette]

    def get_player_effect(self, user_id: str) -> str | None:
        player_skin = self.player_skins.get(user_id, None)
        if player_skin is None or player_skin.effect is None:
            return None

        return player_skin.effect


@dataclass
class DiscordServerConfig:
    dice: dict[str, DiceConfig]

    def has_side(self, side: str) -> bool:
        return side in self.dice

    def get_side_config(self, side: str) -> DiceConfig:
        return self.dice[side]


def parse_discord_server_config(json_obj):
    dice = {}
    for dice_name, dice_config in json_obj.items():
        dice[dice_name] = DiceConfig(
            custom_colors=dice_config["custom_colors"],
            palettes=dice_config["palettes"],
            player_skins=dice_config["player_skins"],
            default_palette=dice_config["default_palette"],
        )

    return DiscordServerConfig(dice=dice)
