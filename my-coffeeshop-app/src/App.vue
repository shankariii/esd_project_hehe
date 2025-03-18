<template>
  <div class="app-container">
    <nav class="navbar">
      <a href="#" class="logo">☕ <span>Brew Haven</span></a>
      <button class="mobile-menu-btn" @click="toggleMenu">☰</button>
      <ul class="nav-links" :class="{ active: mobileMenuOpen }">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/#about">About</router-link></li>
        <li><router-link to="/menu">Menu</router-link></li>
        <li><router-link to="/profile">Profile</router-link></li>
        <li><router-link to="/cart"><i class="fas fa-cart-shopping"></i></router-link></li>
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
export default {
  name: 'App',
  data() {
    return {
      mobileMenuOpen: false
    }
  },
  methods: {
    toggleMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
    }
  }
}
</script>

