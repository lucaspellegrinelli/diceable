import { redisClient } from "$lib/redisConnection";
import { getDefaultConfig } from "../../utils";

export async function POST({ params }) {
    const userUUID = params.user;

    const userExists = await redisClient.hExists('user-configs', userUUID);
    if (!userExists) {
        await redisClient.hSet('user-configs', userUUID, getDefaultConfig(userUUID));
    }

    return new Response();
}
