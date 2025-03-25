<template>
    <div class="menu-container section">
      <div class="search-container">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search drinks..." 
            class="search-input"
            @input="searchDrinks"
          />
          <button class="search-btn">
            <i class="fa fa-search"></i>
          </button>
        </div>
      </div>
  
      <div class="products-grid">
        <div 
          v-for="drink in filteredDrinks" 
          :key="drink.drink_id" 
          class="product-card"
          @click="navigateToDrinkDetail(drink.drink_id)"
        >
          <img :src="drink.image"  :alt="drink.drink_name" class="product-img">
          <div class="product-content">
            <h3 class="product-title">{{ drink.drink_name }}</h3>
            <p class="product-desc">{{ drink.description }}</p>
            <div class="product-footer">
              <p class="product-price">${{ drink.price.toFixed(2) }}</p>
              <button class="add-to-cart-btn">Add to Cart</button>
            </div>
          </div>
        </div>
        
        <div v-if="filteredDrinks.length === 0" class="no-results">
          <p>No drinks match your search. Try another term.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CoffeeMenu',
    data() {
      return {
        drinks: [],
        searchQuery: '',
        loading: true,
        error: null
      };
    },
    computed: {
      filteredDrinks() {
        if (!this.searchQuery) {
          return this.drinks;
        }
        
        const query = this.searchQuery.toLowerCase();
        return this.drinks.filter(drink => {
          return drink.drink_name.toLowerCase().includes(query) || 
                 drink.description.toLowerCase().includes(query);
        });
      }
    },
    methods: {
      async fetchDrinks() {
        try {
          this.loading = true;
          // Replace with your actual API endpoint
          const response = await axios.get('http://127.0.0.1:5002/drinks');
          this.drinks = response.data;
          console.log(this.drinks)
          this.loading = false;
        } catch (err) {
          this.error = 'Failed to load drinks. Please try again later.';
          this.loading = false;
          console.error('Error fetching drinks:', err);
        }
      },
      searchDrinks() {
        // This method exists to allow for debouncing if needed in the future
      },
      navigateToDrinkDetail(drinkId) {
        this.$router.push(`/drink/${drinkId}`);
      }
    },
    created() {
      this.fetchDrinks();
    }
  }
  </script>
  
  <style scoped>
  
  .menu-container {
    padding-top: 6rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .search-container {
    margin-bottom: 2rem;
    display: flex;
    justify-content: center;
  }
  
  .search-box {
    display: flex;
    width: 100%;
    max-width: 600px;
    border-radius: 30px;
    overflow: hidden;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    margin: 0 1rem;
  }
  
  .search-input {
    flex-grow: 1;
    border: none;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    outline: none;
    background-color: white;
  }
  
  .search-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    width: 50px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .search-btn:hover {
    background-color: var(--dark);
  }
  
  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    padding: 0 1rem;
  }
  
  .product-card {
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
  }
  
  .product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
  }
  
  .product-img {
    height: 300px;
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
    height: 60px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    /* -webkit-line-clamp: 3; */
    -webkit-box-orient: vertical;
  }
  
  .product-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
  }
  
  .product-price {
    font-weight: bold;
    color: var(--primary);
    font-size: 1.2rem;
    margin: 0;
  }
  
  .add-to-cart-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .add-to-cart-btn:hover {
    background-color: var(--dark);
  }
  
  .no-results {
    grid-column: 1 / -1;
    text-align: center;
    padding: 2rem;
    color: var(--text-light);
  }
  
  @media (max-width: 768px) {
    .products-grid {
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
  }
  </style>