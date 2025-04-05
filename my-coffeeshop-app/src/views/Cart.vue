<template>
  <div>
    <!-- Cart section -->
    <section class="section">
      <div class="section-heading">
        <!-- <h2>Your Shopping Cart</h2>
        <p>Review your items and proceed to payment</p> -->
      </div>

      <!-- Back to menu link -->
      <div class="cart-container" style="max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
        <a href="http://localhost:5173/menu"
          style="color: var(--primary); display: flex; align-items: center; text-decoration: none; font-weight: 500; margin-bottom: 2rem;">
          <i class="fas fa-arrow-left" style="margin-right: 0.5rem;"></i> Back to Menu
        </a>

        <!-- Outlet information section -->
        <div class="outlet-info"
          style="margin-bottom: 1.5rem; padding: 1rem; background-color: var(--light); border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <p style="font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.25rem;">Ordering from:
              <span style="font-size: 1.1rem; color: var(--dark); font-weight: bold;">
               {{ outletName || 'Select an outlet' }}
              </span>
              <button @click="changeOutlet"
            style="background: none; border: 1px solid var(--primary); color: var(--primary); padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer; font-size: 10px; margin-left: 10px;">
            Change
          </button>
            </p>
          </div>
        </div>

        <!-- Empty cart message -->
        <div v-if="cartItems.length === 0 && !loading" class="empty-cart" style="text-align: center; padding: 3rem 0;">
          <i class="fas fa-shopping-cart" style="font-size: 3rem; color: var(--secondary); margin-bottom: 1rem;"></i>
          <h3 style="margin-bottom: 1rem; color: var(--dark);">Your cart is empty</h3>
          <p style="color: var(--text-light); margin-bottom: 2rem;">Looks like you haven't added any products to your
            cart yet.</p>
          <button @click="proceedToMenu"
            style="background-color: var(--primary); color: white; padding: 0.8rem 1.5rem; border-radius: 5px; text-decoration: none; display: inline-block; ">
            Continue Shopping
          </button>
        </div>

        <!-- Loading state -->
        <div v-if="loading" class="loading" style="text-align: center; padding: 3rem 0;">
          <i class="fas fa-spinner fa-spin" style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;"></i>
          <h3 style="margin-bottom: 1rem; color: var(--dark);">Loading your cart...</h3>
        </div>

        <!-- Cart items and summary in two-column layout that stacks on mobile -->
        <div v-else-if="cartItems.length > 0" class="cart-layout"
          style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
          <!-- Left column: Cart items -->
          <div class="cart-items-column">
            <div class="cart-items">
              <div v-for="(item, index) in cartItems" :key="index" class="cart-item"
                style="display: grid; grid-template-columns: 80px 1fr; gap: 1rem; padding: 1.5rem 0; border-bottom: 1px solid #eee;">
                <!-- Product image -->
                <div class="cart-item-img">
                  <img :src="item.image" :alt="item.name"
                    style="width: 80px; height: 80px; object-fit: cover; border-radius: 5px;">
                </div>

                <!-- Product details -->
                <div class="cart-item-details">
                  <div
                    style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <h3 style="font-size: 1.1rem; color: var(--dark); margin-right: 0.5rem;">{{ item.name }}</h3>
                    <!-- Remove button moved to top right of item details -->
                    <button @click="removeItem(index)"
                      style="background: none; border: none; color: var(--text-light); cursor: pointer; font-size: 1rem; padding: 0;">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                  </div>

                  <!--<p style="font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.8rem;">{{ item.description }}
                  </p>-->

                  <div v-if="item.customizations && item.customizations.length > 0">
                    <p style="font-size: 0.8rem; color: var(--text-light); margin-bottom: 0.5rem;">
                      Customizations:
                    </p>
                    <ul style="list-style-type: none; padding-left: 0; margin-top: 0.25rem;">
                      <li v-for="customization in item.customizations" :key="customization.id"
                        style="font-size: 0.8rem; color: var(--text-light); margin-bottom: 0.25rem;">
                        {{ customization.name }}
                        <span v-if="customization.price_diff > 0"> (+${{ customization.price_diff.toFixed(2) }})</span>
                      </li>
                    </ul>
                  </div>

                  <div
                    style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <!-- Price -->
                    <div class="cart-item-price" style="color: var(--text); font-weight: 500;">
                      ${{ item.price.toFixed(2) }}
                    </div>

                    <!-- Quantity -->
                    <div class="cart-item-quantity" style="display: flex; align-items: center;">
                      <button @click="decrementQuantity(index)"
                        style="background-color: var(--light); border: 1px solid #ddd; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 5px 0 0 5px; cursor: pointer;">
                        <i class="fas fa-minus" style="font-size: 0.8rem;"></i>
                      </button>
                      <input type="number" v-model="item.quantity" min="1"
                        style="width: 40px; height: 30px; border: 1px solid #ddd; border-left: none; border-right: none; text-align: center; outline: none;">
                      <button @click="incrementQuantity(index)"
                        style="background-color: var(--light); border: 1px solid #ddd; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 0 5px 5px 0; cursor: pointer;">
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
            <div class="order-summary"
              style="background-color: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 3px 10px rgba(0,0,0,0.08); position: sticky; top: 20px;">
              <h3 style="font-size: 1.3rem; margin-bottom: 1.5rem; color: var(--dark);">Order Summary</h3>

              <!-- Summary items -->
              <div class="summary-item" style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span>Subtotal</span>
                <span>${{ subtotal.toFixed(2) }}</span>
              </div>

              <!-- <div class="summary-item" style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span>Shipping</span>
                <span>${{ shipping.toFixed(2) }}</span>
              </div> -->

              <div class="summary-item"
                style="display: flex; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
                <span>Tax</span>
                <span>${{ tax.toFixed(2) }}</span>
              </div>

              <!-- Total -->
              <div class="summary-total"
                style="display: flex; justify-content: space-between; margin: 1.5rem 0; font-weight: bold;">
                <span style="font-size: 1.2rem;">Total</span>
                <span style="font-size: 1.2rem; color: var(--primary);">${{ total.toFixed(2) }}</span>
              </div>

              <!-- Proceed to Payment button -->
              <button class="normal-checkout-bar" id="submit" @click="proceedToPayment"
                style="background-color: var(--accent); color: var(--dark); border: none; width: 100%; padding: 1rem; border-radius: 5px; font-weight: bold; margin-top: 1rem; cursor: pointer; transition: background-color 0.3s;">
                Proceed to Payment
              </button>
            </div>
          </div>
        </div>

        <!-- Mobile fixed checkout bar (visible only on small screens) -->
        <div v-if="cartItems.length > 0" class="mobile-checkout-bar"
          style="position: fixed; bottom: 0; left: 0; right: 0; background-color: white; padding: 1rem; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); display: none; align-items: center; justify-content: space-between; z-index: 100;">
          <div class="mobile-total">
            <div style="font-weight: bold; font-size: 1.1rem; color: var(--primary);">${{ total.toFixed(2) }}</div>
            <div style="font-size: 0.8rem; color: var(--text-light);">Total</div>
          </div>
          <button @click="proceedToPayment"
            style="background-color: var(--accent); color: var(--dark); border: none; padding: 0.8rem 1.5rem; border-radius: 5px; font-weight: bold; cursor: pointer;">
            Proceed to Payment
          </button>
        </div>
      </div>
    </section>
  </div>
</template>


<script>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../authStore';  // Import the auth store
import axios from 'axios';

const router = useRouter();
export default {
  data() {
    return {
      cartItems: [],
      // shipping: 0,
      tax: 0,
      loading: true,
      // userId: 'test24', // Replace with dynamic user ID if needed
      outletId: JSON.parse(localStorage.getItem('selectedOutletId')),   // Replace with dynamic outlet ID if needed
      outletName: localStorage.getItem('selectedOutletName'),   // Replace with dynamic outlet ID if needed
      cartId: 0,
      currentTotal: 0,
      apiConfig: {
        cartService: {
          baseURL: 'http://127.0.0.1:5200',
          timeout: 8000
        },
        drinkService: {
          baseURL: 'http://127.0.0.1:5005',
          timeout: 5000
        },
        customService: {
          baseURL: 'http://127.0.0.1:5007',
          timeout: 5000
        }
      }
    };
  },
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    return { authStore, router };
  },
  computed: {
    userId() {
      return this.authStore.user?.uid || null;  // Get user ID from auth store
    },
    subtotal() {
      return this.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },
    total() {
      return this.subtotal + this.tax;
    }
  },
  methods: {
    async fetchCartDetails() {
      try {
        this.loading = true;
        console.log('Starting cart data fetch...');

        // Create axios instances with different configurations
        const cartClient = axios.create({
          baseURL: this.apiConfig.cartService.baseURL,
          timeout: this.apiConfig.cartService.timeout,
          // headers: this.userId ? { 
          //   Authorization: await this.authStore.user.getIdToken() 
          // } : {}
        });

        const drinkClient = axios.create({
          baseURL: this.apiConfig.drinkService.baseURL,
          timeout: this.apiConfig.drinkService.timeout
        });

        const customClient = axios.create({
          baseURL: this.apiConfig.customService.baseURL,
          timeout: this.apiConfig.customService.timeout
        });

        // 1. Fetch cart data
        console.log(`Fetching cart from ${this.apiConfig.cartService.baseURL}`);
        const cartResponse = await cartClient.get(`/get_cart_details/${this.userId}/${this.outletId}`);
        this.cartId = cartResponse.data.data.cart_id
        this.currentTotal = cartResponse.data.data.totalPrice
        console.log('Cart response:', cartResponse.data);

        if (!cartResponse.data?.data?.items) {
          console.warn('No items found in cart');
          this.cartItems = [];
          return;
        }

        // 2. Process each cart item
        this.cartItems = await this.processCartItems(cartResponse.data.data.items, drinkClient, customClient);
        console.log(this.cartItems)
        this.tax = this.subtotal * 0.08;

      } catch (error) {
        console.error('Error in fetchCartDetails:', this.formatAxiosError(error));
        // alert('Failed to load cart. Please try again later.');
      } finally {
        this.loading = false;
      }
    },

    async processCartItems(items, drinkClient, customClient) {

      const processedItems = [];

      for (const [index, item] of items.entries()) {
        try {
          console.log(item)
          console.log(`Processing item ${index + 1}/${items.length}`);

          // Fetch drink details
          const drinkResponse = await drinkClient.get(`/drinks/${item.drink_id}`);
          console.log(`Drink ${item.drink_id} details:`, drinkResponse.data);

          // Fetch customizations if they exist
          let customizations = [];
          if (item.customisations?.length > 0) {
            console.log(`Fetching ${item.customisations.length} customizations...`);
            const customizationPromises = item.customisations.map(c =>
              customClient.get(`/customisations/${c.customisationId_fk}`)
            );
            const customizationResponses = await Promise.all(customizationPromises);
            // cartItemId = customizationResponses.
            customizations = customizationResponses.map(r => ({
              id: r.data.customisation_id,
              name: r.data.name,
              price_diff: r.data.price_diff
            })).sort((a, b) => a.id - b.id);
          }

          processedItems.push({
            id: item.drink_id,
            cart_item_id: item.cart_items_id, // Add this line to store the cart item ID
            name: drinkResponse.data.drink_name,
            description: drinkResponse.data.description || 'No description available',
            price: parseFloat(drinkResponse.data.price) +
              customizations.reduce((sum, c) => sum + c.price_diff, 0),
            quantity: item.quantity || 1,
            image: drinkResponse.data.image || '/placeholder-image.png',
            customizations: customizations
          });

        } catch (error) {
          console.error(`Error processing item ${item.drink_id}:`, this.formatAxiosError(error));
        }
      }

      return processedItems;
    },

    formatAxiosError(error) {
      if (error.response) {
        return `Server error: ${error.response.status} - ${error.response.data}`;
      } else if (error.request) {
        return `No response received: ${error.message}`;
      } else {
        return `Request error: ${error.message}`;
      }
    },

    incrementQuantity(index) {
      this.cartItems[index].quantity++;
      console.log(this.cartItems[index])
      this.updateCart(index);
    },

    decrementQuantity(index) {
      if (this.cartItems[index].quantity > 1) {
        this.cartItems[index].quantity--;
        this.updateCart(index);
      }
    },

    async removeItem(index) {
      try {
        const cartItemId = this.cartItems[index].cart_item_id;
        console.log(cartItemId)
        const response = await axios.delete(
          `http://localhost:5200/delete_cart_item/${cartItemId}`
        );

        // Remove item from local state
        this.cartItems.splice(index, 1);

        // Refresh cart data if needed
        if (response.data.data.cart_deleted) {
          this.fetchCartDetails();
        }

      } catch (error) {
        console.error("Delete failed:", error);
        // Handle error
      }
    },

    async updateCart(index) {
      try {
        const item = this.cartItems[index];
        const cartItemId = item.cart_item_id;
        const newQuantity = item.quantity;

        // Update quantity in backend
        await axios.put(
          `http://localhost:5016/cart_items/${cartItemId}`,
          { quantity: newQuantity }
        );

        // Get current cart total from backend or use local computed total
        // differenceinTotal = item.price
        console.log(item.price)

        // Update cart total in backend (just add one more item's price)
        await axios.put(
          `http://localhost:5015/cart/${this.cartId}`,
          { totalPrice: this.subtotal }
        );

        // UI will update automatically through computed properties

      } catch (error) {
        console.error('Error updating cart:', error);
        this.fetchCartDetails(); // Refresh data
      }
    },


    proceedToPayment() {

      console.log("Proceeding to payment!");
      this.$router.push('/checkout');
    },

    proceedToMenu() {

      console.log("Proceeding to Menu!");
      this.$router.push('/menu');
    },

    changeOutlet() {
      this.$router.push('/findOutlet');
    },
  },
  watch: {
    // Watch for changes in userId or outletId
    userId() {
      this.fetchCartDetails();
    },
    outletId() {
      this.fetchCartDetails();
    }
  },
  created() {
    // this.fetchCartDetails();
    // Initialize auth and then fetch cart
    this.authStore.init().then(() => {
      this.fetchCartDetails();
    });
  }
};
</script>

<!-- Your existing style section remains exactly the same -->
<!-- <style>
/* ... */
</style>y -->

<!-- Mobile-specific CSS -->
<style>
@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 80px 1fr !important;
  }

  .mobile-checkout-bar {
    display: flex !important;
  }

  .normal-checkout-bar {
    display: none;
  }

  .order-summary {
    margin-bottom: 80px !important;
    /* Give space for fixed checkout bar */
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