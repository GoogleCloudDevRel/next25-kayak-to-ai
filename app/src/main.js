import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { useKayakStore } from './store'

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.mount('#app')

// Initialize WebSocket connection after app is mounted
const kayakStore = useKayakStore()
kayakStore.initWebSocket()
