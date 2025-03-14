// src/router.js
import { createRouter, createWebHistory } from 'vue-router'

// Import your page components
import Home from './views/Homepage.vue'
// import About from './views/About.vue'
import Menu from './views/Menu.vue'
import Login from './views/Login.vue'
import DrinkCustomization from './views/DrinkCustomization.vue'
import Cart from './views/Cart.vue'
// import Profile from './views/Profile.vue'
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
    // { 
    //   path: '/profile', 
    //   name: 'profile',
    //   component: Profile 
    // },
    { 
      path: '/cart', 
      name: 'cart',
      component: Cart 
    },
    // Catch-all route for 404 errors
    // { 
    //   path: '/:pathMatch(.*)*', 
    //   name: 'not-found',
    //   component: () => import('./views/NotFound.vue') // Lazy loaded
    // }
  ]
})



export default router