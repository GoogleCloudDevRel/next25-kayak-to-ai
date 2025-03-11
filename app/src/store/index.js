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
        prompt: state.prompt
      }
    }));
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
    code: /*python */ `
# Example 1: List comprehension and string manipulation
names = ['alice', 'bob', 'charlie']
capitalized = [name.title() for name in names]
print(f"Capitalized names: {capitalized}")

# Example 2: Working with dictionaries
student_scores = {
    'Alice': 95,
    'Bob': 87,
    'Charlie': 92
}
avg_score = sum(student_scores.values()) / len(student_scores)
print(f"Average score: {avg_score:.2f}")

# Example 3: Using lambda and filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even_numbers}")`,
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
      if (state.location !== undefined) this.location = state.location;
      if (state.prompt !== undefined) this.prompt = state.prompt;
    },
    
    setIsMoving(isMoving) {
      this.isMoving = isMoving;
      syncWithServer(this);
    },
    
    setPrompt(prompt) {
      this.prompt = prompt;
      this.isMoving = false;
      this.isArrived = false;
      this.location = null;
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
      syncWithServer(this);
    },
  },
});
