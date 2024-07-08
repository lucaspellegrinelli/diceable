require('dotenv').config();
const http = require('http');
const WebSocket = require('ws');
const httpProxy = require('http-proxy');
const cors = require('cors');
const express = require('express');

const SUBURB_HOST = process.env.SUBURB_HOST;
const SUBURB_TOKEN = process.env.SUBURB_TOKEN;
const ORIGIN_SOURCE = process.env.ORIGIN_SOURCE;
const PORT = process.env.PORT || 3000;

if (!SUBURB_HOST || !SUBURB_TOKEN || !ORIGIN_SOURCE) {
  console.error("Environment variables SUBURB_HOST, SUBURB_TOKEN, and ORIGIN_SOURCE must be set");
  process.exit(1);
}

const app = express();
app.use(cors({
  origin: ORIGIN_SOURCE,
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
}));

const server = http.createServer(app);
const wss = new WebSocket.Server({ noServer: true });

wss.on('connection', (ws, request, client) => {
  const suburbUrl = `wss://${SUBURB_HOST}/pubsub/${client.id}/listen`;
  const suburbWs = new WebSocket(suburbUrl, {
    headers: { 'Authorization': SUBURB_TOKEN }
  });

  ws.on('message', message => {
    suburbWs.send(message);
  });

  suburbWs.on('message', message => {
    ws.send(message);
  });

  ws.on('close', () => {
    suburbWs.close();
  });

  suburbWs.on('close', () => {
    ws.close();
  });
});

server.on('upgrade', (request, socket, head) => {
  const { pathname } = new URL(request.url, `http://${request.headers.host}`);
  const parts = pathname.split('/');
  if (parts[1] === 'rolls' && parts[2]) {
    const id = parts[2];

    // Check the origin header
    const origin = request.headers.origin;
    const allowedOrigin = new URL(ORIGIN_SOURCE).hostname;
    const requestOrigin = new URL(origin).hostname;

    if (allowedOrigin !== requestOrigin) {
      socket.destroy();
      return;
    }

    wss.handleUpgrade(request, socket, head, (ws) => {
      ws.client = { id };
      wss.emit('connection', ws, request, { id });
    });
  } else {
    socket.destroy();
  }
});

server.listen(PORT, () => {
  console.log(`Proxy server listening on port ${PORT}`);
});
