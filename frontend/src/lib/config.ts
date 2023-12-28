import type { DiceConfig, LocalDiceConfig, LocalPalette, PlayerSkin } from "./types";

export const INVALID_PALETTE_NAME = 'Unknown';
export const DEFAULT_EFFECT_NAME = 'None';

export const parseServerConfig = (config: DiceConfig): LocalDiceConfig => {
    const palettes: LocalPalette[] = [];
    const playerSkins: PlayerSkin[] = [];

    for (const [paletteName, paletteColors] of Object.entries(config.palettes)) {
        const isDefault = paletteName === config.default_palette;
        palettes.push({ name: paletteName, skin: paletteColors, default: isDefault });
    }

    for (const [discordId, playerSkin] of Object.entries(config.player_skins)) {
        const playerPalette = playerSkin.palette || INVALID_PALETTE_NAME;
        const playerEffect = playerSkin.effect || DEFAULT_EFFECT_NAME;
        const playerDescription = playerSkin.description || '';
        playerSkins.push({
            discordId,
            description: playerDescription,
            palette: playerPalette,
            effect: playerEffect
        });
    }

    return {
        customColors: config.custom_colors === 'true',
        palettes,
        playerSkins
    };
}

export const convertLocalConfig = (config: LocalDiceConfig): DiceConfig => {
    const palettes: { [key: string]: string[] } = {};
    const playerSkins: { [key: string]: PlayerSkin } = {};

    for (const palette of config.palettes) {
        palettes[palette.name] = palette.skin;
    }

    for (const playerSkin of config.playerSkins) {
        playerSkins[playerSkin.discordId] = {
            discordId: playerSkin.discordId,
            description: playerSkin.description || '',
            palette: playerSkin.palette || INVALID_PALETTE_NAME,
            effect: playerSkin.effect || DEFAULT_EFFECT_NAME
        };
    }

    let defaultPalette = config.palettes.find(p => p.default)?.name;
    if (!defaultPalette && Object.keys(palettes).length > 0) {
        defaultPalette = Object.keys(palettes)[0];
    }

    return {
        custom_colors: config.customColors ? 'true' : 'false',
        palettes,
        player_skins: playerSkins,
        default_palette: defaultPalette || ''
    };
}

export const fetchSkinsAndEffects = async (sides: 'd10' | 'd20') => {
    const [effectRes, diceRes] = await Promise.all([
        fetch(`/api/assets/effects/${sides}`),
        fetch(`/api/assets/dice/${sides}`)
    ]);

    const [effects, diceSkins] = await Promise.all([
        effectRes.json(),
        diceRes.json()
    ]);

    return { effects, diceSkins };
}
