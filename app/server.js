import express from 'express';
import { createServer } from 'http';
import { WebSocket, WebSocketServer } from 'ws';

// Initialize Express app
const app = express();
const port = 2999;

// Create HTTP server
const server = createServer(app);

// Create WebSocket server
const wss = new WebSocketServer({ server });

// Store connected clients
const clients = new Set();

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('Client connected');
  clients.add(ws);

  // Handle messages from clients
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message.toString());
      console.log('Received:', data);

      // Broadcast to all other clients
      wss.clients.forEach((client) => {
        console.log('Sending to client', client !== ws, client.readyState === WebSocket.OPEN);
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(data));
        }
      });
    } catch (error) {
      console.error('Error parsing message:', error);
    }
  });

  // Handle client disconnection
  ws.on('close', () => {
    console.log('Client disconnected');
    clients.delete(ws);
  });

  // Send initial connection confirmation
  ws.send(JSON.stringify({ type: 'connected', message: 'Connected to WebSocket server' }));
});

// Start the server
server.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
  console.log(`WebSocket server running on ws://localhost:${port}`);
});
