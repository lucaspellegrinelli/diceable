require('dotenv').config();

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: ['https://bot.togarashi.app', 'http://localhost:3000'],
        methods: ['GET', 'POST'],
        credentials: true
    }
});

io.on('connection', (socket) => {
    console.log('New client connected:', socket.id);

    socket.on('roll', (data) => {
        console.log('roll', JSON.stringify(data));
        io.emit('roll', data);
    });

    socket.on('disconnect', () => console.log('Client disconnected'));
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
