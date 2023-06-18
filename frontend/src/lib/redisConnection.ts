import { env } from '$env/dynamic/private';
import redis from 'redis';

const redisClient = redis.createClient({
    socket: {
        host: env.REDISHOST,
        port: parseInt(env.REDISPORT)
    },
    username: env.REDISUSER,
    password: env.REDISPASSWORD
});

redisClient.connect();

export default redisClient;
