require('dotenv').config();
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const WebSocket = require('ws');
const cors = require('cors');

const allowedOrigins = ['https://bot.togarashi.app', 'http://localhost:3000'];

const app = express();
const server = http.createServer(app);

app.use(cors({
    origin: allowedOrigins,
    methods: ['GET', 'POST'],
    credentials: true
}));

const io = socketIo(server, {
    cors: {
        origin: allowedOrigins,
        methods: ['GET', 'POST'],
        credentials: true
    }
});

const SUBURB_TOKEN = process.env.SUBURB_TOKEN;
const SUBURB_HOST = process.env.SUBURB_HOST;

if (SUBURB_HOST.endsWith('/')) {
    SUBURB_HOST = SUBURB_HOST.slice(0, -1);
}

io.on('connection', (socket) => {
    console.log('New client connected:', socket.id);

    socket.on('join_channel', (data) => {
        console.log('join_channel', JSON.stringify(data));
        const { user_id } = data;
        const channel = `roll-${user_id}`;

        // Create a new WebSocket connection to the suburb server
        const suburbUrl = `${SUBURB_HOST}/pubsub/${channel}/listen`;
        const suburbSocket = new WebSocket(suburbUrl, {
            headers: {
                Authorization: SUBURB_TOKEN
            }
        });

        suburbSocket.on('open', () => {
            console.log(`Connected to suburb server on channel ${channel}`);
        });

        suburbSocket.on('message', (message) => {
            console.log(`Message from suburb server on channel ${channel}: ${message}`);
            const parsedMessage = JSON.parse(message);
            io.to(socket.id).emit(`roll-${user_id}`, parsedMessage);
        });

        suburbSocket.on('close', () => {
            console.log(`Disconnected from suburb server on channel ${channel}`);
        });

        suburbSocket.on('error', (error) => {
            console.error(`Error on suburb server connection for channel ${channel}:`, error);
        });

        // Store the suburb socket in the client socket for future reference
        socket.suburbSocket = suburbSocket;
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
        if (socket.suburbSocket) {
            socket.suburbSocket.close();
        }
    });
});

const port = process.env.PORT || 3000;
server.listen(port, () => console.log(`Listening on port ${port}`));
server.on('error', (err) => console.log(err));

process.on('SIGTERM', () => {
    console.log('SIGTERM signal received: closing HTTP server');
    io.disconnectSockets();
    server.close(() => {
        process.exit(0);
    });
});
