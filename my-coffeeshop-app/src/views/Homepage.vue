

<template>
  <section class="hero" style="padding: 0rem 0rem;">
    <div class="hero-content">
      <h1>Crafting Perfect Moments</h1>
      <p>
        Welcome to Brew Haven, where we believe in the art of exceptional coffee. Every cup tells a story, and we're
        here to make yours memorable.
      </p>
      <!-- <a href="order.html" class="cta-btn">Order Now</a> -->
      <button @click="goToMenu" class="cta-btn">Order Now</button>

    </div>
  </section>

  <!-- Featured Products -->
  <featureProduct></featureProduct>

  <!-- About Section -->
  <section id="about" class="section">
    <div class="about-grid">
      <div class="about-content">
        <h3>Our Story</h3>
        <p>
          Established in 2010, Brew Haven started as a small corner café with a big dream: to create a space where
          coffee isn't just served, but celebrated.
        </p>
        <p>
          Our founder, Hazel Janks, spent years traveling across coffee-growing regions, learning from local farmers
          and perfecting the art of roasting. This journey of discovery and passion is infused in every cup we serve.
        </p>
        <p>
          Today, Brew Haven has grown into a community hub with multiple locations, but our commitment remains the same
          - sourcing ethically, roasting meticulously, and serving joyfully.
        </p>
      </div>
      <div class="about-img-container">
        <img src="../assets/us!.png" alt="Brew Haven Story" class="about-img">
      </div>
    </div>
  </section>

  <!-- Locations -->
  <location></location>

  <!-- Testimonials -->
  <testimonials></testimonials>


  <!-- Newsletter -->
  <section class="newsletter">
    <h2>Stay in the Loop</h2>
    <p>Subscribe to our newsletter for exclusive offers, brewing tips, and updates on seasonal specials.</p>
    <form class="newsletter-form" @submit.prevent="subscribeNewsletter">
      <input type="email" placeholder="Your email address" v-model="email" class="newsletter-input" required>
      <button type="submit" class="newsletter-btn">Subscribe</button>
    </form>
    <p v-if="subscribed" style="margin-top: 1rem; color: var(--primary);">
      Thanks for subscribing! Check your inbox soon.
    </p>
  </section>
</template>


<script setup>
// import HelloWorld from '../components/HelloWorld.vue'
import featureProduct from '../components/featuredProducts.vue'
import testimonials from '../components/testimonials.vue'
import location from '../components/locations.vue'
import { useRouter } from 'vue-router';

const router = useRouter();

const goToMenu = () => {
  router.push('/menu'); // Navigates to the Menu view
};
</script>

<style scoped>
.hero {
  height: 100vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('../src/assets/coffee.webp');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  padding: 0 1rem;
  margin-bottom: 4rem;
}

.hero-content {
  max-width: 800px;
}

.hero h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-btn {
  display: inline-block;
  background-color: var(--accent);
  color: var(--dark);
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  font-weight: bold;
  text-decoration: none;
  border-radius: 30px;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.cta-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 4rem;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}

.about-content {
  padding: 1rem;
}

.about-content h3 {
  font-size: 2rem;
  color: var(--primary);
  margin-bottom: 1.5rem;
}

.about-content p {
  margin-bottom: 1.5rem;
  color: var(--text-light);
}

.about-img-container {
  position: relative;
  height: 100%;
  min-height: 400px;
}

.about-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.newsletter {
      background-color: var(--accent);
      color: var(--dark);
      text-align: center;
      padding: 4rem 2rem;
    }
    
    .newsletter h2 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    
    .newsletter p {
      margin-bottom: 2rem;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }
    
    .newsletter-form {
      max-width: 500px;
      margin: 0 auto;
      display: flex;
    }
    
    .newsletter-input {
      flex: 1;
      padding: 0.8rem 1.5rem;
      border: none;
      border-radius: 30px 0 0 30px;
      font-size: 1rem;
    }
    
    .newsletter-btn {
      background-color: var(--primary);
      color: white;
      border: none;
      padding: 0 1.5rem;
      border-radius: 0 30px 30px 0;
      cursor: pointer;
      font-weight: bold;
    }
</style>
