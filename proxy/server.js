const express = require('express');
const WebSocket = require('ws');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;
const originSource = process.env.ORIGIN_SOURCE;
const suburbHost = process.env.SUBURB_HOST;
const suburbToken = process.env.SUBURB_TOKEN;

const corsOptions = {
    origin: originSource,
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    preflightContinue: false,
    optionsSuccessStatus: 204
};

app.use(cors(corsOptions));

app.use('/rolls/:id', (req, res) => {
    if (!req.headers.upgrade || req.headers.upgrade.toLowerCase() !== 'websocket') {
        res.status(400).send('Invalid request');
        return;
    }

    const wsServer = new WebSocket.Server({ noServer: true });

    wsServer.handleUpgrade(req, req.socket, Buffer.alloc(0), (wsClient) => {
        const { id } = req.params;
        const suburbUrl = `wss://${suburbHost}/pubsub/${id}/listen`;
        const wsSuburb = new WebSocket(suburbUrl, {
            headers: {
                'Authorization': `Bearer ${suburbToken}`
            }
        });

        wsClient.on('message', (message) => {
            wsSuburb.send(message);
        });

        wsSuburb.on('message', (message) => {
            wsClient.send(message);
        });

        wsClient.on('close', () => {
            wsSuburb.close();
        });

        wsSuburb.on('close', () => {
            wsClient.close();
        });

        wsSuburb.on('error', (err) => {
            console.error('Suburb WebSocket error:', err);
            wsClient.close();
        });

        wsClient.on('error', (err) => {
            console.error('Client WebSocket error:', err);
            wsSuburb.close();
        });
    });

    req.socket.on('data', (chunk) => {
        wsServer.handleUpgrade(req, req.socket, chunk, (wsClient) => {
            wsServer.emit('connection', wsClient, req);
        });
    });
});

app.listen(port, () => {
    console.log(`WebSocket proxy server is running on port ${port}`);
});
