<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Reactive state for featured products
const featuredProducts = ref([]);

// Fetch drinks from the API on component mount
const fetchDrinks = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5005/drinks');
    const drinks = response.data;

    // Take only the first 4 drinks
    featuredProducts.value = drinks.slice(0, 4).map(drink => ({
      id: drink.id,
      name: drink.drink_name,
      description: drink.description,
      price: drink.price,
      image: drink.image // Ensure the API provides correct image filenames
    }));
  } catch (error) {
    console.error('Error fetching drinks:', error);
  }
};

onMounted(fetchDrinks);
</script>

<template>
  <section id="menu" class="section featured-products">
    <div class="section-heading">
      <h2>Featured Drinks</h2>
      <p>Discover our most loved coffee creations and seasonal specials.</p>
    </div>
    
    <div class="products-grid">
      <div class="product-card" v-for="product in featuredProducts" :key="product.id">
        <img :src="`/${product.image}`" :alt="product.name" class="product-img">
        <div class="product-content">
          <h3 class="product-title">{{ product.name }}</h3>
          <p class="product-desc">{{ product.description }}</p>
          <div class="product-price">${{ product.price.toFixed(2) }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.featured-products {
  background-color: white;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.product-card {
  background-color: var(--light);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.15);
}

.product-img {
  height: 200px;
  width: 100%;
  object-fit: cover;
}

.product-content {
  padding: 1.5rem;
}

.product-title {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: var(--dark);
}

.product-desc {
  color: var(--text-light);
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.product-price {
  font-weight: bold;
  color: var(--primary);
  font-size: 1.2rem;
}
</style>
