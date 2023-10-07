require('dotenv').config()

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

io.on('connection', (socket) => {
    console.log('New client connected');
    socket.on('disconnect', () => console.log('Client disconnected'));
});

const port = process.env.PORT || 3000;
server.listen(port, () => console.log(`Listening on port ${port}`));