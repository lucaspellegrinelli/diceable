const WebSocket = require('ws');
const http = require('http');
const url = require('url');
const httpProxy = require('http-proxy');

// Environment variables
const targetHost = process.env.SUBURB_HOST;
const authToken = process.env.SUBURB_TOKEN;
const allowedOrigin = process.env.ORIGIN_SOURCE;

const proxy = httpProxy.createProxyServer({});

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('WebSocket proxy server');
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws, req) => {
  const targetUrl = url.resolve(targetHost, req.url);

  // Check the origin
  if (req.headers.origin !== allowedOrigin) {
    ws.close(1008, 'Invalid origin');
    return;
  }

  // Add the authentication token to the headers
  const headers = {
    'Authorization': `Bearer ${authToken}`,
    ...req.headers
  };

  const proxyWs = new WebSocket(targetUrl, null, { headers });

  proxyWs.on('open', () => {
    ws.on('message', (message) => {
      proxyWs.send(message);
    });

    proxyWs.on('message', (message) => {
      ws.send(message);
    });
  });

  proxyWs.on('close', (code, reason) => {
    ws.close(code, reason);
  });

  proxyWs.on('error', (error) => {
    ws.close(1011, 'WebSocket error');
    console.error('WebSocket error:', error);
  });

  ws.on('close', (code, reason) => {
    proxyWs.close(code, reason);
  });

  ws.on('error', (error) => {
    proxyWs.close(1011, 'WebSocket error');
    console.error('WebSocket error:', error);
  });
});

server.listen(8080, () => {
  console.log('WebSocket proxy server is running on port 8080');
});
