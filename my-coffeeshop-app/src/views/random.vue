<template>
    <div class="customize-container section">
      <div v-if="loading" class="loading">
        <p>Loading drink details...</p>
      </div>
      
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <button @click="goBack" class="back-btn">Go Back</button>
      </div>
      
      <div v-else class="customize-content">
        <div class="product-preview">
          <img :src="drink.image" :alt="drink.drink_name" class="product-detail-img">
          <div class="product-info">
            <h2 class="product-detail-title">{{ drink.drink_name }}</h2>
            <p class="product-detail-desc">{{ drink.description }}</p>
            <p class="product-detail-prep">Preparation time: {{ drink.prep_time_min }} minutes</p>
            <p class="product-detail-price">${{ calculateTotalPrice().toFixed(2) }}</p>
          </div>
        </div>
        
        <div class="customization-options">
          <h3 class="options-title">Customize Your Drink</h3>
          
          <div class="option-group">
            <h4>Size</h4>
            <div class="options-buttons">
              <button 
                v-for="size in sizes" 
                :key="size.id"
                :class="['option-btn', { active: selectedSize === size.id }]"
                @click="selectedSize = size.id"
              >
                {{ size.name }} (+${{ size.price.toFixed(2) }})
              </button>
            </div>
          </div>
          
          <div class="option-group">
            <h4>Milk Options</h4>
            <div class="options-buttons">
              <button 
                v-for="milk in milkOptions" 
                :key="milk.id"
                :class="['option-btn', { active: selectedMilk === milk.id }]"
                @click="selectedMilk = milk.id"
              >
                {{ milk.name }} {{ milk.price > 0 ? '(+$' + milk.price.toFixed(2) + ')' : '' }}
              </button>
            </div>
          </div>
          
          <div class="option-group">
            <h4>Extra Shots</h4>
            <div class="quantity-selector">
              <button @click="decrementShots" class="quantity-btn">-</button>
              <span class="quantity-display">{{ extraShots }}</span>
              <button @click="incrementShots" class="quantity-btn">+</button>
            </div>
            <p class="option-price" v-if="extraShots > 0">+${{ (extraShotPrice * extraShots).toFixed(2) }}</p>
          </div>
          
          <div class="option-group">
            <h4>Extras</h4>
            <div class="checkbox-options">
              <div v-for="extra in extras" :key="extra.id" class="checkbox-option">
                <input 
                  type="checkbox" 
                  :id="'extra-' + extra.id" 
                  v-model="selectedExtras" 
                  :value="extra.id"
                >
                <label :for="'extra-' + extra.id">{{ extra.name }} (+${{ extra.price.toFixed(2) }})</label>
              </div>
            </div>
          </div>
          
          <div class="option-group">
            <h4>Special Instructions</h4>
            <textarea 
              v-model="specialInstructions" 
              placeholder="Any special requests for your drink?" 
              class="special-instructions"
            ></textarea>
          </div>
          
          <div class="actions">
            <button @click="goBack" class="back-btn">Back to Menu</button>
            <button @click="addToCart" class="add-to-cart-btn">Add to Cart - ${{ calculateTotalPrice().toFixed(2) }}</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CustomizeDrink',
    data() {
      return {
        drink: null,
        loading: true,
        error: null,
        selectedSize: 2, // Default to medium
        selectedMilk: 1, // Default to regular milk
        extraShots: 0,
        extraShotPrice: 0.75,
        selectedExtras: [],
        specialInstructions: '',
        
        // Options data
        sizes: [
          { id: 1, name: 'Small', price: -0.50 },
          { id: 2, name: 'Medium', price: 0 },
          { id: 3, name: 'Large', price: 0.75 }
        ],
        milkOptions: [
          { id: 1, name: 'Regular', price: 0 },
          { id: 2, name: 'Skim', price: 0 },
          { id: 3, name: 'Almond', price: 0.75 },
          { id: 4, name: 'Oat', price: 0.75 },
          { id: 5, name: 'Soy', price: 0.75 }
        ],
        extras: [
          { id: 1, name: 'Vanilla Syrup', price: 0.50 },
          { id: 2, name: 'Caramel Syrup', price: 0.50 },
          { id: 3, name: 'Hazelnut Syrup', price: 0.50 },
          { id: 4, name: 'Whipped Cream', price: 0.50 },
          { id: 5, name: 'Chocolate Sprinkles', price: 0.25 }
        ]
      };
    },
    methods: {
      async fetchDrinkDetails() {
        try {
          this.loading = true;
          const drinkId = this.$route.params.id;
          // Replace with your actual API endpoint
          const response = await axios.get(`http://127.0.0.1:5002/drinks/${drinkId}`);
          this.drink = response.data;
          this.loading = false;
        } catch (err) {
          this.error = 'Failed to load drink details. Please try again.';
          this.loading = false;
          console.error('Error fetching drink details:', err);
        }
      },
      incrementShots() {
        if (this.extraShots < 5) {
          this.extraShots++;
        }
      },
      decrementShots() {
        if (this.extraShots > 0) {
          this.extraShots--;
        }
      },
      calculateTotalPrice() {
        if (!this.drink) return 0;
        
        let total = this.drink.price;
        
        // Add size cost
        const selectedSizeObj = this.sizes.find(size => size.id === this.selectedSize);
        if (selectedSizeObj) {
          total += selectedSizeObj.price;
        }
        
        // Add milk cost
        const selectedMilkObj = this.milkOptions.find(milk => milk.id === this.selectedMilk);
        if (selectedMilkObj) {
          total += selectedMilkObj.price;
        }
        
        // Add extra shots
        total += this.extraShots * this.extraShotPrice;
        
        // Add extras
        this.selectedExtras.forEach(extraId => {
          const extra = this.extras.find(e => e.id === extraId);
          if (extra) {
            total += extra.price;
          }
        });
        
        return total;
      },
      goBack() {
        this.$router.push('/menu');
      },
      addToCart() {
        // Create an order item object
        const orderItem = {
          drinkId: this.drink.drink_id,
          name: this.drink.drink_name,
          basePrice: this.drink.price,
          size: this.selectedSize,
          milk: this.selectedMilk,
          extraShots: this.extraShots,
          extras: this.selectedExtras,
          specialInstructions: this.specialInstructions,
          totalPrice: this.calculateTotalPrice()
        };
        
        // In a real app, you would dispatch this to a store or make an API call
        console.log('Adding to cart:', orderItem);
        
        // Could use Vuex store or localStorage to save the cart
        let cart = JSON.parse(localStorage.getItem('cart') || '[]');
        cart.push(orderItem);
        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Show confirmation and navigate back to menu
        alert('Added to cart!');
        this.$router.push('/menu');
      }
    },
    created() {
      this.fetchDrinkDetails();
    },
    mounted() {
      // If the route changes but component is reused, refetch data
      this.$watch(
        () => this.$route.params,
        () => {
          this.fetchDrinkDetails();
        }
      );
    }
  }
  </script>
  
  <style scoped>
  .customize-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .loading, .error-message {
    text-align: center;
    padding: 2rem;
    color: var(--text-light);
  }
  
  .customize-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
  
  .product-preview {
    background-color: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  }
  
  .product-detail-img {
    width: 100%;
    height: 250px;
    object-fit: cover;
  }
  
  .product-info {
    padding: 1.5rem;
  }
  
  .product-detail-title {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
    color: var(--dark);
  }
  
  .product-detail-desc {
    color: var(--text-light);
    margin-bottom: 1rem;
    line-height: 1.6;
  }
  
  .product-detail-prep {
    color: var(--text-light);
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }
  
  .product-detail-price {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
    margin-top: 1rem;
  }
  
  .customization-options {
    background-color: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  }
  
  .options-title {
    color: var(--primary);
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
    border-bottom: 2px solid var(--light);
    padding-bottom: 0.5rem;
  }
  
  .option-group {
    margin-bottom: 1.5rem;
  }
  
  .option-group h4 {
    margin-bottom: 0.8rem;
    color: var(--dark);
  }
  
  .options-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .option-btn {
    background-color: var(--light);
    border: 2px solid var(--light);
    border-radius: 5px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .option-btn:hover {
    background-color: var(--accent);
    color: var(--dark);
  }
  
  .option-btn.active {
    background-color: var(--primary);
    border-color: var(--primary);
    color: white;
  }
  
  .quantity-selector {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  
  .quantity-btn {
    width: 30px;
    height: 30px;
    background-color: var(--light);
    border: none;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .quantity-btn:hover {
    background-color: var(--accent);
  }
  
  .quantity-display {
    padding: 0 1rem;
    font-size: 1.1rem;
  }
  
  .option-price {
    color: var(--primary);
    font-weight: bold;
    font-size: 0.9rem;
  }
  
  .checkbox-options {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 0.5rem;
  }
  
  .checkbox-option {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .checkbox-option input[type="checkbox"] {
    accent-color: var(--primary);
  }
  
  .special-instructions {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid var(--light);
    border-radius: 5px;
    min-height: 100px;
    resize: vertical;
  }
  
  .actions {
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
  }
  
  .back-btn {
    background-color: var(--light);
    color: var(--text);
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .back-btn:hover {
    background-color: var(--text-light);
    color: white;
  }
  
  .add-to-cart-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-weight: bold;
  }
  
  .add-to-cart-btn:hover {
    background-color: var(--dark);
  }
  
  @media (max-width: 768px) {
    .customize-content {
      grid-template-columns: 1fr;
    }
    
    .checkbox-options {
      grid-template-columns: 1fr;
    }
  }
  </style>