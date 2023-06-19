import redisClient from "$lib/redisConnection";


const get_default_config = (userUUID: string) => (JSON.stringify({
    "custom_colors": "false",
    "palettes": {
        "Default": ["red", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "indigo", "green"]
    },
    "player_skins": {
        [userUUID]: { "palette": "Default", "description": "You" }
    },
    "default_palette": "Default"
}));

export async function POST({ params, body }) {
    const userUUID = params.user;

    const userExists = await redisClient.hExists('user-configs', userUUID);
    if (!userExists) {
        await redisClient.hSet('user-configs', userUUID, get_default_config(userUUID));
    }

    return new Response();
}
