// src/router.js
import { createRouter, createWebHistory } from 'vue-router'

// Import your page components
import Home from './views/Homepage.vue'
// import About from './views/About.vue'
import Menu from './views/Menu.vue'
import Login from './views/Login.vue'
import DrinkCustomization from './views/DrinkCustomization.vue'
import Cart from './views/Cart.vue'
import Profile from './views/Profile.vue'
import TrackOrders from './views/TrackOrders.vue'
import Checkout from './views/Checkout.vue'
import FindOutlet from './views/FindOutlet.vue'
// import Cart from './views/Cart.vue'

// Create and export the router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { 
      path: '/', 
      name: 'home',
      component: Home 
    },
    { 
      path: '/login', 
      name: 'login',
      component: Login 
    },
    { 
      path: '/menu', 
      name: 'menu',
      component: Menu 
    },
    {
      path: '/drink/:id',
      name: 'drink',
      component: DrinkCustomization
    },
    { 
      path: '/profile', 
      name: 'profile',
      component: Profile 
    },
    { 
      path: '/cart', 
      name: 'cart',
      component: Cart 
    },
    { 
      path: '/trackOrders', 
      name: 'trackOrders',
      component: TrackOrders 
    },
    { 
      path: '/homepage/#about', 
      name: 'about',
    },
    { 
      path: '/checkout', 
      name: 'checkout',
      component: Checkout 
    },
    { 
      path: '/findOutlet', 
      name: 'findOutlet',
      component: FindOutlet 
    },
    // Catch-all route for 404 errors
    { 
      path: '/:pathMatch(.*)*', 
      name: 'not-found',
      component: () => import('./views/404Error.vue') // Lazy loaded
    }
  ]
})



export default router