// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './firebase'
import axios from 'axios';

// Configure Axios
axios.defaults.baseURL = import.meta.env.VITE_API_URL || '';

// Create and mount the app
const app = createApp(App)
app.use(router)
app.mount('#app')