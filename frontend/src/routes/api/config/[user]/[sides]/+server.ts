import { redisClient } from '$lib/redisConnection';
import type { DiceConfig, UserConfig } from '$lib/types';
import { getDefaultDiceConfig, getDefaultConfig } from '../../utils';

const diceSideCount: { [key: string]: number } = {
    "d10": 10,
    "d20": 20
};

export async function GET({ params }) {
    const userUUID = params.user;
    const diceSides = params.sides;

    let userConfig = await redisClient.hGet('user-configs', userUUID);

    if (!userConfig) {
        await redisClient.hSet('user-configs', userUUID, getDefaultConfig(userUUID));
        userConfig = await redisClient.hGet('user-configs', userUUID);
    }

    const userConfigJson = JSON.parse(userConfig);

    if (!(diceSides in userConfigJson)) {
        return new Response(`Dice sides ${diceSides} not found`);
    }

    const diceUserConfig = userConfigJson[diceSides];
    return new Response(JSON.stringify(diceUserConfig));
}

export async function POST({ params, request }) {
    const userUUID = params.user;
    const diceSides = params.sides;
    const config: DiceConfig = await request.json();

    const userExists = await redisClient.hExists('user-configs', userUUID);
    let userFullConfigStr: string | undefined = undefined;
    if (userExists) {
        userFullConfigStr = await redisClient.hGet('user-configs', userUUID);
    }

    let userFullConfig: UserConfig | undefined = undefined;
    if (userFullConfigStr) {
        userFullConfig = JSON.parse(userFullConfigStr);
    }

    if (!userFullConfig) {
        userFullConfig = {};
    }

    let diceUserConfig: DiceConfig | undefined = undefined;
    if (userFullConfig && diceSides in userFullConfig) {
        diceUserConfig = userFullConfig[diceSides];
    }

    const defaultConfig = getDefaultDiceConfig(diceSideCount[diceSides], userUUID);
    const currentConfig: DiceConfig = diceUserConfig || defaultConfig;

    // Remove any palettes that don't exist
    const palettes = Object.keys(config.palettes);
    Object.keys(config.player_skins).forEach((player) => {
        const playerPalette = config.player_skins[player].palette;
        if (!palettes.includes(playerPalette)) {
            delete config.player_skins[player];
        }
    });

    // Update userConfig with the currentConfig
    userFullConfig[diceSides] = {
        ...currentConfig,
        ...config
    };

    await redisClient.hSet('user-configs', userUUID, JSON.stringify(userFullConfig));
    return new Response(JSON.stringify(userFullConfig[diceSides]));
}
