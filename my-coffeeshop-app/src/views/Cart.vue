<template>
    <div>
      <!-- Cart section -->
      <section class="section">
        <div class="section-heading">
          <h2>Your Shopping Cart</h2>
          <p>Review your items and proceed to payment</p>
        </div>
  
        <!-- Back to menu link -->
        <div class="cart-container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
          <a href="products.html" style="color: var(--primary); display: flex; align-items: center; text-decoration: none; font-weight: 500; margin-bottom: 2rem;">
            <i class="fas fa-arrow-left" style="margin-right: 0.5rem;"></i> Back to Menu
          </a>
  
          <!-- Empty cart message -->
          <div v-if="cartItems.length === 0" class="empty-cart" style="text-align: center; padding: 3rem 0;">
            <i class="fas fa-shopping-cart" style="font-size: 3rem; color: var(--secondary); margin-bottom: 1rem;"></i>
            <h3 style="margin-bottom: 1rem; color: var(--dark);">Your cart is empty</h3>
            <p style="color: var(--text-light); margin-bottom: 2rem;">Looks like you haven't added any products to your cart yet.</p>
            <a href="products.html" style="background-color: var(--primary); color: white; padding: 0.8rem 1.5rem; border-radius: 5px; text-decoration: none; display: inline-block;">
              Continue Shopping
            </a>
          </div>
  
          <!-- Cart items and summary in two-column layout that stacks on mobile -->
          <div v-else class="cart-layout" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <!-- Left column: Cart items -->
            <div class="cart-items-column">
              <div class="cart-items">
                <div v-for="(item, index) in cartItems" :key="index" class="cart-item" style="display: grid; grid-template-columns: 80px 1fr; gap: 1rem; padding: 1.5rem 0; border-bottom: 1px solid #eee;">
                  <!-- Product image -->
                  <div class="cart-item-img">
                    <img :src="item.image" :alt="item.name" style="width: 80px; height: 80px; object-fit: cover; border-radius: 5px;">
                  </div>
                  
                  <!-- Product details -->
                  <div class="cart-item-details">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                      <h3 style="font-size: 1.1rem; color: var(--dark); margin-right: 0.5rem;">{{ item.name }}</h3>
                      <!-- Remove button moved to top right of item details -->
                      <button @click="removeItem(index)" style="background: none; border: none; color: var(--text-light); cursor: pointer; font-size: 1rem; padding: 0;">
                        <i class="fas fa-trash-alt"></i>
                      </button>
                    </div>
                    
                    <p style="font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.8rem;">{{ item.description }}</p>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                      <!-- Price -->
                      <div class="cart-item-price" style="color: var(--text); font-weight: 500;">
                        ${{ item.price.toFixed(2) }}
                      </div>
                      
                      <!-- Quantity -->
                      <div class="cart-item-quantity" style="display: flex; align-items: center;">
                        <button @click="decrementQuantity(index)" style="background-color: var(--light); border: 1px solid #ddd; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 5px 0 0 5px; cursor: pointer;">
                          <i class="fas fa-minus" style="font-size: 0.8rem;"></i>
                        </button>
                        <input type="number" v-model="item.quantity" min="1" style="width: 40px; height: 30px; border: 1px solid #ddd; border-left: none; border-right: none; text-align: center; outline: none;">
                        <button @click="incrementQuantity(index)" style="background-color: var(--light); border: 1px solid #ddd; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 0 5px 5px 0; cursor: pointer;">
                          <i class="fas fa-plus" style="font-size: 0.8rem;"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Right column: Order summary -->
            <div class="order-summary-column">
              <div class="order-summary" style="background-color: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 3px 10px rgba(0,0,0,0.08); position: sticky; top: 20px;">
                <h3 style="font-size: 1.3rem; margin-bottom: 1.5rem; color: var(--dark);">Order Summary</h3>
                
                <!-- Summary items -->
                <div class="summary-item" style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                  <span>Subtotal</span>
                  <span>${{ subtotal.toFixed(2) }}</span>
                </div>
                
                <div class="summary-item" style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                  <span>Shipping</span>
                  <span>${{ shipping.toFixed(2) }}</span>
                </div>
                
                <div class="summary-item" style="display: flex; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
                  <span>Tax</span>
                  <span>${{ tax.toFixed(2) }}</span>
                </div>
                
                <!-- Total -->
                <div class="summary-total" style="display: flex; justify-content: space-between; margin: 1.5rem 0; font-weight: bold;">
                  <span style="font-size: 1.2rem;">Total</span>
                  <span style="font-size: 1.2rem; color: var(--primary);">${{ total.toFixed(2) }}</span>
                </div>
                
                <!-- Proceed to Payment button -->
                <button class="normal-checkout-bar" id="submit" @click="proceedToPayment" style="background-color: var(--accent); color: var(--dark); border: none; width: 100%; padding: 1rem; border-radius: 5px; font-weight: bold; margin-top: 1rem; cursor: pointer; transition: background-color 0.3s;">
                  Proceed to Payment
                </button>
              </div>
            </div>
          </div>
          
          <!-- Mobile fixed checkout bar (visible only on small screens) -->
          <div v-if="cartItems.length > 0" class="mobile-checkout-bar" style="position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 1rem; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); display: none; align-items: center; justify-content: space-between; z-index: 100;">
            <div class="mobile-total">
              <div style="font-weight: bold; font-size: 1.1rem; color: var(--primary);">${{ total.toFixed(2) }}</div>
              <div style="font-size: 0.8rem; color: var(--text-light);">Total</div>
            </div>
            <button @click="proceedToPayment" style="background-color: var(--accent); color: var(--dark); border: none; padding: 0.8rem 1.5rem; border-radius: 5px; font-weight: bold; cursor: pointer;">
              Proceed to Payment
            </button>
          </div>
        </div>
      </section>
  
      
    </div>
  </template>
  
  <script>
  import { useRouter } from 'vue-router';
  export default {
    data() {
      return {
        cartItems: [
          {
            id: 1,
            name: "Ethiopian Yirgacheffe Coffee",
            description: "Light roast with floral and citrus notes",
            price: 14.99,
            quantity: 2,
            image: "/api/placeholder/80/80"
          },
          {
            id: 2,
            name: "Stainless Steel French Press",
            description: "Double-wall insulated, 34 oz capacity",
            price: 34.99,
            quantity: 1,
            image: "/api/placeholder/80/80"
          },
          {
            id: 3,
            name: "Ceramic Pour-Over Dripper",
            description: "Hand-crafted ceramic dripper with ribbed design",
            price: 24.99,
            quantity: 1,
            image: "/api/placeholder/80/80"
          }
        ],
        shipping: 5.99,
        tax: 0
      };
    },
    computed: {
      subtotal() {
        return this.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
      },
      total() {
        return this.subtotal + this.shipping + this.tax;
      }
    },
    methods: {
      incrementQuantity(index) {
        this.cartItems[index].quantity++;
      },
      decrementQuantity(index) {
        if (this.cartItems[index].quantity > 1) {
          this.cartItems[index].quantity--;
        }
      },
      removeItem(index) {
        this.cartItems.splice(index, 1);
      },
      
      proceedToPayment() {
        const router = useRouter();
        // In a real application, this would redirect to a payment page
        console.log("Proceeding to payment!");
        router.push(`/checkout`)
      }
    },
    created() {
      // Calculate tax (assuming 8% tax rate)
      this.tax = this.subtotal * 0.08;
    }
  };

  
  </script>
  <!-- Mobile-specific CSS -->
  <style>
  @media (max-width: 768px) {
    .cart-item {
      grid-template-columns: 80px 1fr !important;
    }
    
    .mobile-checkout-bar {
      display: flex !important;
    }

    .normal-checkout-bar{
        display: none;
    }
    
    .order-summary {
      margin-bottom: 80px !important; /* Give space for fixed checkout bar */
    }
    
    .section-heading h2 {
      font-size: 1.8rem !important;
    }
    
    .section-heading p {
      font-size: 1rem !important;
    }
    
    .section {
      padding: 3rem 1rem !important;
    }
  }
</style>