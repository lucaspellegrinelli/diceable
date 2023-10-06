import { redisClient } from '$lib/redisConnection';
import { getDefaultDiceConfig } from '../../utils';

type UserDiceConfig = {
    custom_colors: string,
    palettes: { [key: string]: string[] },
    player_skins: { [key: string]: { palette: string, effect: string } }
};

const diceSideCount: { [key: string]: number } = {
    "d10": 10,
    "d20": 20
};

export async function GET({ params }) {
    const userUUID = params.user;
    const diceSides = params.sides;
    const userConfig = await redisClient.hGet('user-configs', userUUID);

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
    const config: UserDiceConfig = await request.json();

    const userExists = await redisClient.hExists('user-configs', userUUID);
    let userFullConfigStr = undefined;
    if (userExists) {
        userFullConfigStr = await redisClient.hGet('user-configs', userUUID);
    }

    let userFullConfig = undefined;
    if (userFullConfigStr) {
        userFullConfig = JSON.parse(userFullConfigStr);
    }

    let diceUserConfig = undefined;
    if (userFullConfig && diceSides in userFullConfig) {
        diceUserConfig = userFullConfig[diceSides];
    }

    const defaultConfig = getDefaultDiceConfig(diceSideCount[diceSides], userUUID);
    const currentConfig: UserDiceConfig = JSON.parse(diceUserConfig || defaultConfig);

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
