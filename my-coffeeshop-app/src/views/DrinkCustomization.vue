<template>
    <div class="customization-container">
      <!-- Back button and header -->
      <div class="back-nav">
        <button class="back-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i> Back to Menu
        </button>
      </div>
  
      <div class="product-container" v-if="drink">
        <div class="product-image-section">
          <img :src="drink.image" :alt="drink.name" class="product-image">
        </div>
  
        <div class="product-details">
          <h1 class="product-title">{{ drink.name }}</h1>
          <p class="product-description">{{ drink.description }}</p>
          
          <div class="customization-section">
            <!-- Size selection -->
            <div class="option-group">
              <h3 class="option-title">Size</h3>
              <div class="size-options">
                <div 
                  v-for="size in sizes" 
                  :key="size.id"
                  :class="['size-option', { active: selectedSize === size.id }]"
                  @click="selectSize(size.id)"
                >
                  <div class="size-visual">
                    <img src="../assets/coffee_icon.png" :style="{ height: size.visualHeight + 'px'}">
                  </div>
                  
                  <div class="size-info">
                    <span class="size-name">{{ size.name }}</span>
                    <span class="size-price">+${{ size.priceDiff.toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Milk selection -->
            <div class="option-group">
              <h3 class="option-title">Milk Options</h3>
              <div class="radio-options">
                <div 
                  v-for="milk in milkOptions" 
                  :key="milk.id"
                  :class="['radio-option', { active: selectedMilk === milk.id }]"
                  @click="selectMilk(milk.id)"
                >
                  <div class="radio-button">
                    <div class="radio-inner" v-if="selectedMilk === milk.id"></div>
                  </div>
                  <div class="option-info">
                    <span class="option-name">{{ milk.name }}</span>
                    <span class="option-price" v-if="milk.priceDiff > 0">+${{ milk.priceDiff.toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Add-ons selection -->
            <div class="option-group">
              <h3 class="option-title">Add-ons</h3>
              <div class="checkbox-options">
                <div 
                  v-for="addon in addonOptions" 
                  :key="addon.id"
                  :class="['checkbox-option', { active: selectedAddons.includes(addon.id) }]"
                  @click="toggleAddon(addon.id)"
                >
                  <div class="checkbox">
                    <i class="fas fa-check" v-if="selectedAddons.includes(addon.id)"></i>
                  </div>
                  <div class="option-info">
                    <span class="option-name">{{ addon.name }}</span>
                    <span class="option-price">+${{ addon.price.toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Quantity selector -->
          <div class="quantity-section">
            <h3 class="option-title">Quantity</h3>
            <div class="quantity-controls">
              <button 
                class="quantity-btn" 
                @click="decrementQuantity" 
                :disabled="quantity <= 1"
              >
                <i class="fas fa-minus"></i>
              </button>
              <span class="quantity-value">{{ quantity }}</span>
              <button class="quantity-btn" @click="incrementQuantity">
                <i class="fas fa-plus"></i>
              </button>
            </div>
          </div>
          
          <!-- Price summary and add to cart -->
          <div class="price-summary">
            <div class="price-calculation">
              <div class="base-price">
                <span>Base price:</span>
                <span>${{ drink.price.toFixed(2) }}</span>
              </div>
              <div class="size-price" v-if="sizePriceDiff > 0">
                <span>Size upgrade:</span>
                <span>+${{ sizePriceDiff.toFixed(2) }}</span>
              </div>
              <div class="milk-price" v-if="milkPriceDiff > 0">
                <span>Milk option:</span>
                <span>+${{ milkPriceDiff.toFixed(2) }}</span>
              </div>
              <div class="addons-price" v-if="addonsTotalPrice > 0">
                <span>Add-ons:</span>
                <span>+${{ addonsTotalPrice.toFixed(2) }}</span>
              </div>
              <div class="item-total">
                <span>Item total:</span>
                <span>${{ itemTotal.toFixed(2) }}</span>
              </div>
              <div class="order-total">
                <span><strong>Order total:</strong></span>
                <span><strong>${{ orderTotal.toFixed(2) }}</strong></span>
              </div>
            </div>
            
            <button class="add-to-cart-btn" @click="addToCart">
              Add to Cart <i class="fas fa-shopping-cart"></i>
            </button>
          </div>
        </div>
      </div>
      
      <div v-else class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading drink details...</p>
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
  .customization-container {
    background-color: var(--light);
    min-height: 100vh;
    padding: 2rem 1rem 4rem;
  }
  
  .back-nav {
    max-width: 1200px;
    margin: 0 auto 2rem;
  }
  
  .back-btn {
    background: none;
    border: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1rem;
    color: var(--primary);
    cursor: pointer;
    padding: 0.5rem 0;
  }
  
  .back-btn:hover {
    color: var(--dark);
  }
  
  .product-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .product-image-section {
    width: 100%;
    height: 300px;
    overflow: hidden;
  }
  
  .product-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .product-details {
    padding: 2rem;
  }
  
  .product-title {
    font-size: 2rem;
    color: var(--dark);
    margin-bottom: 0.5rem;
  }
  
  .product-description {
    color: var(--text-light);
    margin-bottom: 2rem;
    line-height: 1.6;
  }
  
  .customization-section {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  
  .option-group {
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding-bottom: 2rem;
  }
  
  .option-title {
    font-size: 1.2rem;
    color: var(--primary);
    margin-bottom: 1rem;
  }
  
  /* Size selection */
  .size-options {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
  }
  
  .size-option {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s;
    padding: 1rem;
    border-radius: 8px;
    border: 2px solid transparent;
    min-width: 100px;
  }
  
  .size-option.active {
    border-color: var(--primary);
    background-color: rgba(93, 64, 55, 0.05);
  }
  
  .size-visual {
    width: 40px;
    /* background-color: var(--primary); */
    border-radius: 4px;
    margin-bottom: 0.75rem;
  }
  
  .size-info {
    text-align: center;
  }
  
  .size-name {
    display: block;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }
  
  .size-price {
    color: var(--primary);
    font-size: 0.9rem;
  }
  
  /* Radio options for milk */
  .radio-options {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .radio-option {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .radio-option:hover {
    background-color: rgba(93, 64, 55, 0.05);
  }
  
  .radio-option.active {
    background-color: rgba(93, 64, 55, 0.05);
  }
  
  .radio-button {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .radio-inner {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--primary);
  }
  
  .option-info {
    display: flex;
    justify-content: space-between;
    flex: 1;
  }
  
  .option-name {
    font-weight: 500;
  }
  
  .option-price {
    color: var(--primary);
    font-weight: 600;
  }
  
  /* Checkbox options for add-ons */
  .checkbox-options {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  .checkbox-option {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .checkbox-option:hover {
    background-color: rgba(93, 64, 55, 0.05);
  }
  
  .checkbox-option.active {
    background-color: rgba(93, 64, 55, 0.05);
  }
  
  .checkbox {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary);
  }
  
  /* Special instructions */
  .instructions-input {
    width: 100%;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    min-height: 100px;
    resize: vertical;
  }
  
  .instructions-input:focus {
    outline: none;
    border-color: var(--primary);
  }
  
  /* Quantity selector */
  .quantity-section {
    margin: 2rem 0;
  }
  
  .quantity-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 180px;
  }
  
  .quantity-btn {
    width: 40px;
    height: 40px;
    background-color: var(--light);
    border: none;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .quantity-btn:hover:not([disabled]) {
    background-color: var(--secondary);
    color: white;
  }
  
  .quantity-btn[disabled] {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .quantity-value {
    flex: 1;
    text-align: center;
    font-weight: 600;
    font-size: 1.2rem;
  }
  
  /* Price summary and add to cart */
  .price-summary {
    margin-top: 2rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    padding-top: 2rem;
  }
  
  .price-calculation {
    margin-bottom: 2rem;
  }
  
  .price-calculation > div {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .item-total {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px dashed rgba(0, 0, 0, 0.1);
  }
  
  .order-total {
    font-size: 1.2rem;
    margin-top: 0.5rem;
    color: var(--primary);
  }
  
  .add-to-cart-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .add-to-cart-btn:hover {
    background-color: var(--dark);
  }
  
  /* Loading state */
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
  }
  
  .loading-spinner {
    width: 50px;
    height: 50px;
    border: 5px solid rgba(93, 64, 55, 0.2);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  /* Responsive adjustments */
  @media (min-width: 768px) {
    .product-container {
      flex-direction: row;
    }
    
    .product-image-section {
      width: 40%;
      height: auto;
    }
    
    .product-details {
      width: 60%;
    }
  }
  
  @media (max-width: 767px) {
    .product-image-section {
      height: 200px;
    }
    
    .size-options {
      justify-content: space-between;
    }
    
    .size-option {
      min-width: 80px;
    }
    
    .checkbox-options {
      grid-template-columns: 1fr;
    }
  }
  </style>