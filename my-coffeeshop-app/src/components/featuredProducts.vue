<script setup>
import { ref } from 'vue'

// defineProps({
//   msg: String,
// })

const featuredProducts = ref([
          {
            id: 1,
            name: 'Signature Espresso',
            description: 'Our bold and balanced house espresso with rich notes of chocolate and caramel.',
            price: 3.49
          },
          {
            id: 2,
            name: 'Vanilla Latte',
            description: 'Smooth espresso with steamed milk and our house-made vanilla syrup.',
            price: 4.99
          },
          {
            id: 3,
            name: 'Cold Brew',
            description: 'Coffee steeped for 24 hours for a smooth, rich flavor with low acidity.',
            price: 4.49
          },
          {
            id: 4,
            name: 'Seasonal Spiced Chai',
            description: 'Black tea infused with warming spices and steamed with your choice of milk.',
            price: 4.79
          }
        ]);
</script>

<template>
      <section id="menu" class="section featured-products">
      <div class="section-heading">
        <h2>Featured Drinks</h2>
        <p>Discover our most loved coffee creations and seasonal specials.</p>
      </div>
      
      <div class="products-grid">
        <div class="product-card" v-for="product in featuredProducts" :key="product.id">
          <img :src="`/api/placeholder/400/300?text=${encodeURIComponent(product.name)}`" :alt="product.name" class="product-img">
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
