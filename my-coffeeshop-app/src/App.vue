<template>
  <div class="app-container">
    <nav class="navbar">
      <a href="/" class="logo">☕ <span>Brew Haven</span></a>
      <button class="mobile-menu-btn" @click="toggleMenu">☰</button>
      <ul class="nav-links" :class="{ active: mobileMenuOpen }">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/#about">About</router-link></li>
        <li><router-link to="/menu">Menu</router-link></li>
        <!-- Conditional rendering for profile/login -->
        <li v-if="isLoggedIn"><router-link to="/profile">Profile</router-link></li>
        <li v-else><router-link to="/login">Login</router-link></li>
        <!-- Cart with item count -->
        <li>
          <router-link to="/cart" class="cart-link">
            <i class="fas fa-cart-shopping"></i>
            <span v-if="cartItemCount > 0" class="cart-count">{{ cartItemCount }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <main>
      <!-- This is where route components will be rendered -->
      <router-view />
    </main>

    <footer>
      <div class="footer-content">
        <div class="footer-column">
          <h3>Brew Haven</h3>
          <p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 1rem;">
            Crafting Perfect Moments, One Cup at a Time.
          </p>
          <div class="social-links">
            <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-linkedin-in"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
            <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
          </div>
        </div>

        <div class="footer-column">
          <h3>Quick Links</h3>
          <ul class="footer-links">
            <li><a href="#">Home</a></li>
            <li><a href="#about">Our Story</a></li>
            <li><a href="#menu">Menu</a></li>
            <li><a href="order.html">Order Online</a></li>
            <li><a href="#locations">Locations</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h3>Contact</h3>
          <ul class="footer-links">
            <li>info@brewhaven.com</li>
            <li>(555) 123-4567</li>
            <li>123 Coffee Street</li>
            <li>Beantown, CT 45678</li>
          </ul>
        </div>

        <div class="footer-column">
          <h3>Hours</h3>
          <ul class="footer-links">
            <li>Monday - Friday: 6am - 8pm</li>
            <li>Saturday: 7am - 9pm</li>
            <li>Sunday: 7am - 6pm</li>
          </ul>
        </div>
      </div>

      <div class="copyright">
        &copy; 2025 Brew Haven. All Rights Reserved.
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      mobileMenuOpen: false,
      isLoggedIn: false, // Set this based on your auth logic
      cartItemCount: 0, // Initialize to 0
      user_id: "test24",
      outletId: JSON.parse(localStorage.getItem('selectedOutletId'))
    }
  },
  methods: {
    toggleMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    },
    async fetchCartItemCount() {
      try {
        // Replace 'test24/24' with your actual user ID or dynamic values
        const response = await axios.get(`http://localhost:5200/get_cart_item_count/${this.user_id}/${this.outletId}`);
        // const cartResponse = await cartClient.get(`/get_cart_details/${this.userId}/${this.outletId}`);

        
        if (response.data.code === 200) {
          this.cartItemCount = response.data.data.item_count;
        } else {
          console.error('Error fetching cart count:', response.data);
        }
      } catch (error) {
        console.error('Error fetching cart count:', error);
      }
    }
  },
  created() {
    // Fetch cart count when component is created
    this.fetchCartItemCount();
    
    // Optional: Set up polling to keep cart count updated
    // this.polling = setInterval(this.fetchCartItemCount, 30000); // Update every 30 seconds
  },
  beforeUnmount() {
    // Clean up polling if used
    // if (this.polling) clearInterval(this.polling);
  }
}
</script>

<style>
/* Add these styles to your existing CSS */
.cart-link {
  position: relative;
  display: inline-block;
}

.cart-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #e74c3c;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}
</style>