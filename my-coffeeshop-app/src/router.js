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
import Random from './views/random.vue'
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
      component: DrinkCustomization,
      meta: { requiresAuth: true }
    },
    { 
      path: '/profile', 
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    { 
      path: '/cart', 
      name: 'cart',
      component: Cart,
      meta: { requiresAuth: true }
    },
    { 
      path: '/trackOrders', 
      name: 'trackOrders',
      component: TrackOrders,
      meta: { requiresAuth: true }
    },
    // { 
    //   path: '/homepage/#about', 
    //   name: 'about',
    // },
    { 
      path: '/checkout', 
      name: 'checkout',
      component: Checkout,
      meta: { requiresAuth: true }
    },
    { 
      path: '/findOutlet', 
      name: 'findOutlet',
      component: FindOutlet
    },
    { 
      path: '/random/:id', 
      name: 'random',
      component: Random 
    },
    // Catch-all route for 404 errors
    { 
      path: '/:pathMatch(.*)*', 
      name: 'not-found',
      component: () => import('./views/404Error.vue') // Lazy loaded
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
    return savedPosition || { top: 0 }
  }
})

export default router