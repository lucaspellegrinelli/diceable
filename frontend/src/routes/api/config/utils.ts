import type { DiceConfig } from "$lib/types";

export const getDefaultDiceConfig = (sides: number, userUUID: string): DiceConfig => {
    // Validate sides parameter
    if (!sides || sides < 3 || !Number.isInteger(sides)) {
        throw new Error(`Invalid sides parameter: ${sides}. Must be a positive integer >= 3.`);
    }

    return {
        custom_colors: "false",
        palettes: {
            "Default": ["red", ...Array(sides - 2).fill("indigo"), "green"]
        },
        player_skins: {
            [userUUID]: {
                discordId: userUUID,
                description: "You",
                palette: "Default",
                effect: "None"
            }
        },
        default_palette: "Default"
    };
};

export const getDefaultConfig = (userUUID: string) => (JSON.stringify({
    "d10": getDefaultDiceConfig(10, userUUID),
    "d20": getDefaultDiceConfig(20, userUUID)
}));
