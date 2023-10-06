import { redisClient } from '$lib/redisConnection';

type UserConfig = {
    custom_colors: string,
    palettes: { [key: string]: string[] },
    player_skins: { [key: string]: { palette: string, effect: string } }
};

const get_default_config = (userUUID: string) => (JSON.stringify({
    "custom_colors": "false",
    "palettes": {
        "Default": ["red", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "green"]
    },
    "player_skins": {
        userUUID: { "palette": "Default" }
    },
    "default_palette": "Default"
}));

export async function GET({ params }) {
    const userUUID = params.user;
    const userConfig = await redisClient.hGet('user-configs', userUUID);
    return new Response(userConfig);
}

export async function POST({ params, request }) {
    const userUUID = params.user;
    const config: UserConfig = await request.json();

    const userExists = await redisClient.hExists('user-configs', userUUID);
    let userConfig = undefined;
    if (userExists) {
        userConfig = await redisClient.hGet('user-configs', userUUID);
    }

    const defaultConfig = get_default_config(userUUID);
    const currentConfig: UserConfig = JSON.parse(userConfig || defaultConfig);

    // Remove any palettes that don't exist
    const palettes = Object.keys(config.palettes);
    Object.keys(config.player_skins).forEach((player) => {
        const playerPalette = config.player_skins[player].palette;
        if (!palettes.includes(playerPalette)) {
            delete config.player_skins[player];
        }
    });

    // Update userConfig with the currentConfig
    const newConfig = {
        ...currentConfig,
        ...config
    };

    await redisClient.hSet('user-configs', userUUID, JSON.stringify(newConfig));
    return new Response(JSON.stringify(newConfig));
}
