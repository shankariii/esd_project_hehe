// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { initializeApp } from 'firebase/app'
import { createPinia } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './authStore' // Adjust the path as needed

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCvIDqbUMswOpiUuhK4T5F1xDtV6TF3DhY",
    authDomain: "esd-coffeehouse.firebaseapp.com",
    projectId: "esd-coffeehouse",
    storageBucket: "esd-coffeehouse.firebasestorage.app",
    messagingSenderId: "775228208734",
    appId: "1:775228208734:web:e789da4fb8fd39b6d6e6cf",
    measurementId: "G-6Q5J1S1KLP"
};

// Initialize Firebase
initializeApp(firebaseConfig);

// Configure Axios
axios.defaults.baseURL = import.meta.env.VITE_API_URL || '';

// Create app instance
const app = createApp(App)

// Initialize Pinia
const pinia = createPinia()
app.use(pinia)

// Initialize auth store
const authStore = useAuthStore()

// Wait for auth initialization before mounting the app
authStore.init().then(() => {
  // Setup navigation guards
  router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    
    if (requiresAuth && !authStore.isAuthenticated) {
      // Redirect to login if trying to access protected route
      next('/login');
    } else if (to.path === '/login' && authStore.isAuthenticated) {
      // Redirect to homepage if already logged in
      next('/findOutlet');
    } else {
      next();
    }
  });
  
  // Mount the app
  app.use(router)
  app.mount('#app')
})