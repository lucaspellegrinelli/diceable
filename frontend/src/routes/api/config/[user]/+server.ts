import { redisClient } from "$lib/redisConnection";
import type { UserConfig } from "vite";
import { getDefaultConfig } from "../utils";

export async function GET({ params }) {
    const userUUID = params.user;

    let userConfig: string = await redisClient.hGet('user-configs', userUUID);

    if (!userConfig) {
        await redisClient.hSet('user-configs', userUUID, getDefaultConfig(userUUID));
        userConfig = await redisClient.hGet('user-configs', userUUID);
    }

    const userConfigJson: UserConfig = JSON.parse(userConfig);
    return new Response(JSON.stringify(userConfigJson));
}
