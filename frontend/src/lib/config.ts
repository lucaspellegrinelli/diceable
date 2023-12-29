import type { DiceConfig, LocalDiceConfig, LocalPalette, PlayerSkin } from "./types";

export const INVALID_PALETTE_NAME = 'Unknown';
export const DEFAULT_EFFECT_NAME = 'None';

export const updateCurrentConfig = async (user: string, sides: 'd10' | 'd20', fetchFunc?: any) => {
    if (!fetchFunc) {
        fetchFunc = fetch;
    }

    const [effectRes, diceRes, configRes] = await Promise.all([
        fetchFunc(`/api/assets/effects/${sides}`),
        fetchFunc(`/api/assets/dice/${sides}`),
        fetchFunc(`/api/config/${user}/${sides}`)
    ]);

    const [effects, diceSkins, config]: [string[], string[], DiceConfig] = await Promise.all([
        effectRes.json(),
        diceRes.json(),
        configRes.json()
    ]);

    return {
        effects,
        diceSkins,
        config: parseServerConfig(config)
    };
}

export const saveConfig = async (user: string, sides: 'd10' | 'd20', config: LocalDiceConfig) => {
    const serverDiceConfig = convertLocalConfig(config);
    const url = `/api/config/${user}/${sides}`;

    await fetch(url, {
        method: 'POST',
        body: JSON.stringify(serverDiceConfig)
    });
}

const convertLocalConfig = (config: LocalDiceConfig): DiceConfig => {
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

const parseServerConfig = (config: DiceConfig): LocalDiceConfig => {
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
