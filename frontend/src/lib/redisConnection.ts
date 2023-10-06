import { env } from '$env/dynamic/private';
import redis from 'redis';

export const redisClient = redis.createClient({
    socket: {
        host: env.REDISHOST,
        port: parseInt(env.REDISPORT)
    },
    username: env.REDISUSER,
    password: env.REDISPASSWORD
});

export const redisPubsubClient = redis.createClient({
    socket: {
        host: env.REDISHOST,
        port: parseInt(env.REDISPORT)
    },
    username: env.REDISUSER,
    password: env.REDISPASSWORD
});

redisClient.connect();
redisPubsubClient.connect();

redisClient.on('error', (error) => {
    console.error(error);
});

redisPubsubClient.on('error', (error) => {
    console.error(error);
});