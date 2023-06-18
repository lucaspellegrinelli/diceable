import { Server } from 'socket.io';

import redis from 'redis';

export default function injectSocketIO(server) {
    const io = new Server(server);

    const redisClient = redis.createClient({
        socket: {
            host: process.env.REDISHOST || 'redis',
            port: parseInt(process.env.REDISPORT || '6379')
        },
        username: process.env.REDISUSER || 'default',
        password: process.env.REDISPASSWORD || 'password'
    });

    redisClient.on('connect', () => {
        console.log(`Redis client connected`);
    });

    redisClient.on('error', (err) => {
        console.log(`Redis error: ${err}`);
    });

    redisClient.on('end', () => {
        console.log('Redis client disconnected');
    });

    redisClient.subscribe('rolls', (message) => {
        console.log(`Received message: ${message}`);
        io.emit('rolls', JSON.parse(message));
    });

    redisClient.connect();

    console.log('SocketIO injected');
}
