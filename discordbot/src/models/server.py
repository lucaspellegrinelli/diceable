from dataclasses import dataclass
import json
from typing import Optional


@dataclass
class PlayerSkin:
    discordId: str
    palette: str
    description: Optional[str]
    effect: Optional[str]

    @staticmethod
    def from_json(json_obj) -> "PlayerSkin":
        return PlayerSkin(
            discordId=json_obj["discordId"],
            palette=json_obj["palette"],
            description=json_obj.get("description", None),
            effect=json_obj.get("effect", None),
        )


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

    @staticmethod
    def from_json(json_obj) -> "DiceConfig":
        return DiceConfig(
            custom_colors=json_obj["custom_colors"],
            palettes=json_obj["palettes"],
            player_skins={
                skin_id: PlayerSkin.from_json(skin)
                for skin_id, skin in json_obj["player_skins"].items()
            },
            default_palette=json_obj["default_palette"],
        )


@dataclass
class DiscordServerConfig:
    dice: dict[str, DiceConfig]

    def has_side(self, side: str) -> bool:
        return side in self.dice

    def get_side_config(self, side: str) -> DiceConfig:
        return self.dice[side]

    def to_json(self) -> str:
        return json.dumps({
            dice_name: {
                "custom_colors": dice_config.custom_colors,
                "palettes": dice_config.palettes,
                "player_skins": dice_config.player_skins,
                "default_palette": dice_config.default_palette,
            }
            for dice_name, dice_config in self.dice.items()
        })

    @staticmethod
    def from_json(json_str: str) -> "DiscordServerConfig":
        json_obj = json.loads(json_str)
        return DiscordServerConfig(
            dice={
                dice_name: DiceConfig.from_json(dice_config)
                for dice_name, dice_config in json_obj.items()
            }
        )

    @staticmethod
    def default() -> "DiscordServerConfig":
        return DiscordServerConfig(dice={
            f"d{sides}": DiceConfig(
                custom_colors="false",
                palettes={
                    "default": ["blue"] * sides,
                },
                player_skins={},
                default_palette="default",
            )
            for sides in [10, 20]
        })
