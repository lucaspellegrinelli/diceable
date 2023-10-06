export const getDefaultDiceConfig = (sides: number, userUUID: string) => ({
    "custom_colors": "false",
    "palettes": {
        "Default": ["red", ...Array(sides - 2).fill("indigo"), "green"]
    },
    "player_skins": {
        [userUUID]: { "palette": "Default", "description": "You" }
    },
    "default_palette": "Default"
});

export const getDefaultConfig = (userUUID: string) => (JSON.stringify({
    "d10": getDefaultDiceConfig(10, userUUID),
    "d20": getDefaultDiceConfig(20, userUUID)
}));
