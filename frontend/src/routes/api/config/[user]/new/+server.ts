import redisClient from "$lib/redisConnection";

const get_default_config = () => (JSON.stringify({
    "custom_colors": "false",
    "palettes": {}, // { "PALETTE_NAME": ["color", "color", ...] }
    "player_skins": {}, // { "DISCORD_ID": { "palette": None, "effect": None } }
}));

export async function POST({ params, body }) {
    const userUUID = params.user;

    const userExists = await redisClient.hExists('user-configs', userUUID);
    if (!userExists) {
        await redisClient.hSet('user-configs', userUUID, get_default_config());
    }

    return new Response();
}
