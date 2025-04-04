<template>
  <div class="drink-customization">
    <!-- Popup Box -->
    <div v-if="isPopupVisible" class="popup-overlay">
      <div class="popup-box">
        <h3>{{ popupTitle }}</h3>
        <p>{{ popupMessage }}</p>
        <button @click="closePopup" class="popup-button">OK</button>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading" style="text-align: center; padding: 3rem 0;">
      <i class="fas fa-spinner fa-spin" style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;"></i>
      <h3 style="margin-bottom: 1rem; color: var(--dark);">Loading drink options...</h3>
    </div>
    <div v-else>
      <div class="content-wrapper">
        <!-- Main Content Column -->
        <div class="main-content">
          <!-- Drink Header Section -->
          <a @click="goBack">
            <i class="fas fa-arrow-left"></i> <!-- FontAwesome arrow icon -->
          </a>
          <div class="drink-header">
            <div class="drink-image-container">
              <img :src="'/' + drink.image" :alt="drink.drink_name" class="drink-image" />
            </div>
            <div class="drink-details">
              <h2>{{ drink.drink_name }}</h2>
              <p>{{ drink.description }}</p>
              <p><strong>Price:</strong> ${{ drink.price.toFixed(2) }}</p>
            </div>
          </div>
          <!-- Customization Options -->
          <div class="customization-options">
            <!-- Size Options -->
            <div class="customization-section">
              <h3>Size</h3>
              <div class="options-container">
                <div
                  v-for="size in sizeOptions"
                  :key="size.customisation_id"
                  class="option-button"
                  :class="{ 'option-selected': selectedSize.customisation_id === size.customisation_id }"
                  @click="selectedSize = size"
                >
                  {{ size.name }} (+${{ size.price_diff.toFixed(2) }})
                </div>
              </div>
            </div>
            <!-- Milk Options -->
            <div class="customization-section">
              <h3>Milk Options</h3>
              <div class="options-container">
                <div
                  v-for="milk in milkOptions"
                  :key="milk.customisation_id"
                  class="option-button"
                  :class="{ 'option-selected': selectedMilk.customisation_id === milk.customisation_id }"
                  @click="selectedMilk = milk"
                >
                  {{ milk.name }}
                  <span v-if="milk.price_diff > 0">(+${{ milk.price_diff.toFixed(2) }})</span>
                </div>
              </div>
            </div>
            <!-- Extra Shots -->
            <div class="customization-section">
              <h3>Quantity</h3>
              <div class="counter-container">
                <button class="counter-button" @click="decrementQuantity" :disabled="quantity <= 1">-</button>
                <span class="counter-value">{{ quantity }}</span>
                <button class="counter-button" @click="incrementQuantity">+</button>
              </div>
            </div>
            <!-- Add-ons / Extras -->
            <div class="customization-section">
              <h3>Extras</h3>
              <div class="checkbox-options">
                <div v-for="addon in addons" :key="addon.customisation_id" class="checkbox-option">
                  <input type="checkbox" :id="addon.name" :value="addon" v-model="selectedAddons" />
                  <label :for="addon.name">{{ addon.name }} (+${{ addon.price_diff.toFixed(2) }})</label>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Sidebar with Order Summary -->
        <div class="order-summary-sidebar">
          <div class="order-summary">
            <h3>Order Summary</h3>
            <div class="summary-content">
              <div class="summary-item">
                <span class="item-label">Drink:</span>
                <span class="item-value">{{ drink.drink_name }}</span>
              </div>
              <div class="summary-item">
                <span class="item-label">Size:</span>
                <span class="item-value">{{ selectedSize.name }}</span>
              </div>
              <div class="summary-item">
                <span class="item-label">Milk:</span>
                <span class="item-value">{{ selectedMilk.name }}</span>
              </div>
              <div class="summary-item">
                <span class="item-label">Quantity:</span>
                <span class="item-value">{{ quantity }}</span>
              </div>
              <div class="summary-item">
                <span class="item-label">Add-ons:</span>
                <span class="item-value">{{ selectedAddons.map(a => a.name).join(', ') || 'None' }}</span>
              </div>
              <div class="summary-divider"></div>
              <div class="summary-item total">
                <span class="item-label">Total Price:</span>
                <span class="item-value">${{ totalPrice.toFixed(2) }}</span>
              </div>
            </div>
            <!-- Navigation Buttons -->
            <div class="navigation-buttons">
              <button @click="goBack" class="back-btn">Back</button>
              <button @click="addToCart" class="add-btn">Add to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useAuthStore } from '../authStore'; // Import the auth store

export default {
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      drink: {}, // Holds the drink details
      drinkId: '',
      sizeOptions: [], // Holds size customizations
      milkOptions: [], // Holds milk customizations
      addons: [], // Holds add-ons
      selectedSize: {}, // Selected size
      selectedMilk: {}, // Selected milk
      selectedAddons: [], // Selected add-ons
      quantity: 1, // Number of extra shots
      specialInstructions: '', // Special instructions
      loading: true, // Loading state
      error: null, // Error state

      // Popup state
      isPopupVisible: false,
      popupTitle: '',
      popupMessage: '',
    };
  },
  computed: {
    userId() {
      return this.authStore.user?.uid || null; // Get user ID from auth store
    },
    // Calculate the total price dynamically
    totalPrice() {
      let total = this.drink.price;
      total += this.selectedSize.price_diff || 0;
      total += this.selectedMilk.price_diff || 0;
      total += this.selectedAddons.reduce((sum, addon) => sum + addon.price_diff, 0);
      total = total * this.quantity;
      return total;
    },
  },
  async created() {
    try {
      this.loading = true;
      await this.authStore.init(); // Initialize auth first
      if (!this.authStore.isAuthenticated) {
        this.$router.push('/login');
        return;
      }
      // Fetch drink details
      this.drinkId = this.$route.params.id;
      const drinkResponse = await axios.get(`http://127.0.0.1:5005/drinks/${this.drinkId}`);
      this.drink = drinkResponse.data;
      // Fetch all customization options in parallel
      const [sizeResponse, milkResponse, addonsResponse] = await Promise.all([
        axios.get('http://127.0.0.1:5007/customisations/type/S'),
        axios.get('http://127.0.0.1:5007/customisations/type/M'),
        axios.get('http://127.0.0.1:5007/customisations/type/A'),
      ]);
      this.sizeOptions = sizeResponse.data;
      this.milkOptions = milkResponse.data;
      this.addons = addonsResponse.data;
      // Set default selections
      this.selectedSize = this.sizeOptions[0];
      this.selectedMilk = this.milkOptions[0];
    } catch (error) {
      console.error('Error loading drink customization:', error);
      this.error = 'Failed to load drink options. Please try again later.';
    } finally {
      this.loading = false;
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1); // Navigate back
    },
    showPopup(title, message) {
      this.popupTitle = title;
      this.popupMessage = message;
      this.isPopupVisible = true;
    },
    closePopup() {
      this.isPopupVisible = false;
    },
    async addToCart() {
      if (!this.userId) {
        this.showPopup('Login Required', 'Please login to add items to cart');
        return;
      }
      try {
        const cartItemCustomisation = [
          ...this.selectedAddons.map(addon => ({ customisationId_fk: addon.customisation_id })),
        ];
        if (this.selectedSize.customisation_id) {
          cartItemCustomisation.push({ customisationId_fk: this.selectedSize.customisation_id });
        }
        if (this.selectedMilk.customisation_id) {
          cartItemCustomisation.push({ customisationId_fk: this.selectedMilk.customisation_id });
        }

        const payload = {
          cart: {
            user_id: this.userId,
            outlet_id: JSON.parse(localStorage.getItem('selectedOutletId')),
            totalPrice: parseFloat(this.totalPrice),
          },
          cart_items: [
            {
              drink_id: this.drink.drink_id,
              quantity: this.quantity,
            },
          ],
          cart_item_customisation: cartItemCustomisation,
        };

        const response = await axios.post('http://127.0.0.1:5200/add_to_cart', payload);

        if (response.data && response.data.data && response.data.data.cart_id) {
          const cartId = response.data.data.cart_id;
          this.showPopup('Success', `Cart created successfully! Cart ID: ${cartId}`);
          setTimeout(() => {
            this.$router.push('/menu').then(() => {
              window.location.reload();
            });
          }, 2000); // Delay navigation by 2 seconds
        } else {
          this.showPopup('Error', 'Failed to create cart. Please try again.');
        }
      } catch (error) {
        console.error('Error creating cart:', error);
        if (error.response) {
          this.showPopup('Error', `Error: ${error.response.data.message || 'Failed to create cart.'}`);
        } else {
          this.showPopup('Network Error', 'Network error. Please check your connection.');
        }
      }
    },
    incrementQuantity() {
      this.quantity += 1;
    },
    decrementQuantity() {
      if (this.quantity > 1) {
        this.quantity -= 1;
      }
    },
  },
};
</script>

<style scoped>
/* Existing styles */
.drink-customization {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 6%;
  background-color: var(--light);
}
.content-wrapper {
  display: flex;
  gap: 6rem;
}
.main-content {
  flex: 1;
  min-width: 0;
}
.order-summary-sidebar {
  width: 350px;
  flex-shrink: 0;
  align-self: flex-start;
  position: sticky;
  top: 6rem;
}
.drink-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: flex-start;
  margin-top: 30px;
}
.drink-image-container {
  flex: 0 0 300px;
}
.drink-image {
  width: 100%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.drink-details {
  flex: 1;
  text-align: left;
}
.drink-details h2 {
  color: var(--primary);
  margin-bottom: 0.75rem;
  font-size: 2rem;
}
.drink-details p {
  margin-bottom: 0.75rem;
  line-height: 1.6;
  color: var(--text);
}
.customization-options {
  display: grid;
  gap: 2rem;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  background-color: #f9f9f9;
}
.customization-section {
  padding: 1.5rem;
}
.customization-section h3 {
  color: var(--primary);
  margin-bottom: 1rem;
  font-size: 1.5rem;
}
.options-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.option-button {
  padding: 0.75rem 1.25rem;
  background-color: var(--light);
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}
.option-button:hover {
  background-color: #e9e3e0;
}
.option-selected {
  background-color: var(--primary);
  color: white;
}
.counter-container {
  display: flex;
  align-items: center;
  width: fit-content;
}
.counter-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--light);
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.counter-button:hover:not(:disabled) {
  background-color: #e9e3e0;
}
.counter-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.counter-value {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 500;
  margin: 0 0.5rem;
}
.checkbox-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.75rem;
}
.checkbox-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.checkbox-option input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}
.checkbox-option label {
  cursor: pointer;
}
.order-summary {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #eaeaea;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.order-summary h3 {
  color: var(--primary);
  margin-bottom: 1.25rem;
  font-size: 1.5rem;
  border-bottom: 2px solid var(--primary);
  padding-bottom: 0.75rem;
  position: relative;
}
.summary-content {
  padding: 0.5rem;
  flex: 1;
}
.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.85rem;
  align-items: flex-start;
}
.item-label {
  font-weight: 600;
  color: #555;
  flex: 0 0 40%;
}
.item-value {
  text-align: right;
  color: #333;
  flex: 0 0 60%;
  word-break: break-word;
}
.summary-divider {
  height: 1px;
  background-color: #eaeaea;
  margin: 1rem 0;
}
.summary-item.total {
  margin-top: 0.5rem;
  font-size: 1.25rem;
}
.summary-item.total .item-label {
  color: var(--primary);
}
.summary-item.total .item-value {
  font-weight: 700;
  color: var(--primary);
}
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 1.5rem;
}
.navigation-buttons button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}
.back-btn {
  background-color: #e0e0e0;
  color: var(--text);
}
.back-btn:hover {
  background-color: #d0d0d0;
}
.add-btn {
  background-color: var(--primary);
  color: white;
}
.add-btn:hover {
  background-color: var(--secondary);
}

/* Popup styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.popup-box {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}
.popup-box h3 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: var(--primary);
}
.popup-box p {
  margin-bottom: 1.5rem;
  font-size: 1rem;
  color: var(--text);
}
.popup-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}
.popup-button:hover {
  background-color: var(--secondary);
}

@media (max-width: 1024px) {
  .content-wrapper {
    flex-direction: column;
  }
  .order-summary-sidebar {
    width: 100%;
    position: static;
  }
}
@media (max-width: 768px) {
  .drink-header {
    flex-direction: column;
  }
  .drink-image-container {
    flex: 0 0 auto;
    width: 100%;
    margin-bottom: 1rem;
  }
  .options-container {
    flex-direction: column;
  }
  .option-button {
    width: 100%;
  }
  .checkbox-options {
    grid-template-columns: 1fr;
  }
  .summary-item {
    flex-direction: column;
    margin-bottom: 1rem;
  }
  .item-label {
    margin-bottom: 0.25rem;
    flex: 0 0 100%;
  }
  .item-value {
    flex: 0 0 100%;
    text-align: left;
  }
}
</style>