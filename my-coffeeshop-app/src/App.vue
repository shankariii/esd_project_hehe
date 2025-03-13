<template>
  <div class="app-container">
    <nav class="navbar">
      <a href="#" class="logo">☕ <span>Brew Haven</span></a>
      <button class="mobile-menu-btn" @click="toggleMenu">☰</button>
      <ul class="nav-links" :class="{ active: mobileMenuOpen }">
        <!-- <li><a href="#">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#">Menu</a></li>
        <li><a href="#">Profile</a></li>
        <li><a href="#">
            <i class="fas fa-cart-shopping"></i>
          </a></li> -->
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
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
<style>
.navbar {
  background-color: var(--primary);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.logo span {
  margin-left: 0.5rem;
}

.nav-links {
  display: flex;
  list-style: none;
}

.nav-links li {
  margin-left: 2rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: var(--accent);
}

.footer {
  background-color: var(--dark);
  color: white;
  padding: 4rem 2rem 2rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto 3rem;
}

.footer-column h3 {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  color: var(--accent);
}

.footer-links {
  list-style: none;
}

.footer-links li {
  margin-bottom: 0.8rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.social-icon {
  display: inline-block;
  width: 40px;
  height: 40px;
  background-color: var(--accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.social-icon:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.copyright {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}
</style>
