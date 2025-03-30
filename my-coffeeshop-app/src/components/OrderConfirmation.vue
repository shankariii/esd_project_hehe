<template>
    <div class="confirmation-overlay" v-if="show">
      <div class="confirmation-modal">
        <div class="confirmation-header">
          <h2>Order Confirmed!</h2>
          <div class="confirmation-icon">✓</div>
        </div>
        
        <div class="confirmation-details">
          <div class="confirmation-message">
            <p>Thank you for your order! Your payment has been processed successfully.</p>
            <p class="payment-id">Payment ID: {{ paymentId }}</p>
            <p class="timestamp">{{ timestamp }}</p>
          </div>
          
          <div class="order-summary">
            <h3>Order Summary</h3>
            
            <div class="order-items">
              <div class="order-item" v-for="(item, index) in items" :key="index">
                <div class="item-details">
                  <h4>{{ item.name }}</h4>
                  <div v-if="item.customizations && item.customizations.length > 0">
                    <p class="customizations-label">Customizations:</p>
                    <ul class="customizations-list">
                      <li v-for="customization in item.customizations" :key="customization.id">
                        {{ customization.name }}
                        <span v-if="customization.price_diff > 0">(+${{ customization.price_diff.toFixed(2) }})</span>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="item-price">
                  ${{ (item.price * item.quantity).toFixed(2) }}
                  <div class="quantity">{{ item.quantity }} × ${{ item.price.toFixed(2) }}</div>
                </div>
              </div>
            </div>
            
            <div class="summary-calculations">
              <div class="summary-line">
                <span>Subtotal</span>
                <span>${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="summary-line">
                <span>Taxes</span>
                <span>${{ tax.toFixed(2) }}</span>
              </div>
              <div class="summary-total">
                <span>TOTAL</span>
                <span>${{ total.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="confirmation-actions">
          <button class="view-order-btn" @click="goToOrderHistory">View Order History</button>
          <button class="close-btn" @click="close">Go To Home</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: {
        type: Boolean,
        required: true
      },
      paymentId: {
        type: String,
        required: true
      },
      items: {
        type: Array,
        required: true
      },
      subtotal: {
        type: Number,
        required: true
      },
      tax: {
        type: Number,
        required: true 
      },
      total: {
        type: Number,
        required: true
      }
    },
    
    data() {
      return {
        timestamp: new Date().toLocaleString()
      };
    },
    
    methods: {
      close() {
        this.$emit('close');
      },
      
      goToOrderHistory() {
        // Navigate to order history page
        this.$router.push('/profile');
        // this.close();
      },
      goToMenu() {
        // Navigate to order history page
        this.$router.push('/');
        // this.close();
      }
    }
  }
  </script>
  
  <style scoped>
  :root {
    --primary: #5D4037;
    --secondary: #8D6E63;
    --accent: #FFCA28;
    --light: #EFEBE9;
    --dark: #3E2723;
    --text: #212121;
    --text-light: #757575;
  }
  
  .confirmation-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .confirmation-modal {
    background-color: white;
    width: 90%;
    max-width: 600px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
  }
  
  .confirmation-header {
    background-color: var(--primary);
    color: white;
    padding: 1.5rem;
    text-align: center;
    position: relative;
  }
  
  .confirmation-header h2 {
    margin: 0;
    font-size: 1.8rem;
  }
  
  .confirmation-icon {
    background-color: var(--accent);
    color: var(--primary);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 1rem auto 0;
  }
  
  .confirmation-details {
    padding: 1.5rem;
    overflow-y: auto;
  }
  
  .confirmation-message {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .payment-id {
    font-size: 0.9rem;
    color: var(--text-light);
    margin-top: 0.5rem;
  }
  
  .timestamp {
    font-size: 0.8rem;
    color: var(--text-light);
  }
  
  .order-summary {
    background-color: #f8f8f8;
    border-radius: 8px;
    padding: 1.5rem;
  }
  
  .order-summary h3 {
    margin-top: 0;
    color: var(--primary);
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }
  
  .order-items {
    margin-bottom: 1.5rem;
  }
  
  .order-item {
    display: flex;
    justify-content: space-between;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid #eee;
  }
  
  .order-item:last-child {
    border-bottom: none;
  }
  
  .item-details {
    flex: 1;
  }
  
  .item-details h4 {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
  }
  
  .customizations-label {
    font-size: 0.8rem;
    color: var(--text-light);
    margin: 0.25rem 0;
  }
  
  .customizations-list {
    list-style-type: none;
    padding-left: 0.5rem;
    margin: 0.25rem 0;
  }
  
  .customizations-list li {
    font-size: 0.8rem;
    color: var(--text-light);
    margin-bottom: 0.25rem;
  }
  
  .item-price {
    font-weight: 600;
    text-align: right;
  }
  
  .quantity {
    font-size: 0.8rem;
    color: var(--text-light);
    font-weight: normal;
  }
  
  .summary-calculations {
    border-top: 1px solid #ddd;
    padding-top: 1rem;
  }
  
  .summary-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }
  
  .summary-total {
    display: flex;
    justify-content: space-between;
    font-weight: 600;
    font-size: 1.2rem;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #ddd;
  }
  
  .confirmation-actions {
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    border-top: 1px solid #eee;
  }
  
  .view-order-btn, .close-btn {
    padding: 0.8rem;
    border-radius: 4px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    flex: 1;
  }
  
  .view-order-btn {
    background-color: var(--primary);
    color: white;
  }
  
  .view-order-btn:hover {
    background-color: var(--dark);
  }
  
  .close-btn {
    background-color: #f0f0f0;
    color: var(--text);
  }
  
  .close-btn:hover {
    background-color: #e0e0e0;
  }
  
  @media (max-width: 768px) {
    .confirmation-actions {
      flex-direction: column;
    }
  }
  </style>