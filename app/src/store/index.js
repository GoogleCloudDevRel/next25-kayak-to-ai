import { defineStore } from "pinia";

// WebSocket connection
let socket = null;
let reconnectInterval = null;
const WEBSOCKET_URL = 'ws://localhost:2999';

// Connect to WebSocket server
const connectWebSocket = (store) => {
  // Clear any existing reconnect interval
  if (reconnectInterval) {
    clearInterval(reconnectInterval);
  }

  // Create new WebSocket connection
  socket = new WebSocket(WEBSOCKET_URL);

  // Connection opened
  socket.addEventListener('open', () => {
    console.log('Connected to WebSocket server');
    store.connected = true;
  });

  // Listen for messages
  socket.addEventListener('message', (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log('Message from server:', data);

      // Handle different types of messages
      if (data.type === 'stateUpdate') {
        // Update store state without triggering another sync
        store.updateFromServer(data.state);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  });

  // Connection closed
  socket.addEventListener('close', () => {
    console.log('Disconnected from WebSocket server. Attempting to reconnect...');
    store.connected = false;
    // Attempt to reconnect every 5 seconds
    reconnectInterval = setInterval(() => {
      if (socket.readyState === WebSocket.CLOSED) {
        connectWebSocket(store);
      }
    }, 5000);
  });

  // Connection error
  socket.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
  });
};

// Send state update to server
const syncWithServer = (state) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    console.log('Syncing with server', state);
    socket.send(JSON.stringify({
      type: 'stateUpdate',
      state: {
          route: state.route,
          isMoving: state.isMoving,
          isArrived: state.isArrived,
          location: state.location,
          prompt: state.prompt,
          code: state.code,
        },
      }),
    )
  }
};

export const useKayakStore = defineStore('kayak', {
  state: () => ({
    connected: false,
    route: 'intro',
    isMoving: false,
    isArrived: false,
    location: null,
    prompt: 'Prompt selected previously',
    code: null,
  }),
  actions: {
    // Initialize WebSocket connection
    initWebSocket() {
      connectWebSocket(this);
    },

    // Update state from server without triggering sync
    updateFromServer(state) {
      if (state.route !== undefined) this.route = state.route;
      if (state.isMoving !== undefined) this.isMoving = state.isMoving;
      if (state.isArrived !== undefined) this.isArrived = state.isArrived;
      if (state.location !== undefined && this.location === null) {
        this.location = state.location;
      }
      if (state.prompt !== undefined) this.prompt = state.prompt;
      if (state.code !== undefined) this.code = state.code;
    },

    setIsMoving(isMoving) {
      this.isMoving = isMoving;
      syncWithServer(this);
    },

    setCode(code) {
      this.code = code;
      syncWithServer(this);
    },

    setPrompt(prompt) {
      this.prompt = prompt;
      this.isMoving = false;
      this.isArrived = false;
      this.location = null;
      this.code = null;
      syncWithServer(this);
    },

    setArrived(isArrived) {
      this.isArrived = isArrived;
      syncWithServer(this);
    },

    setLocation(location) {
      this.location = location;
      syncWithServer(this);
    },

    setRoute(route) {
      this.route = route;
      syncWithServer(this);
    },

    reset() {
      this.isMoving = false;
      this.isArrived = false;
      this.prompt = 'Prompt selected previously';
      this.location = null;
      this.code = null;
      syncWithServer(this);
    },
  },
});
