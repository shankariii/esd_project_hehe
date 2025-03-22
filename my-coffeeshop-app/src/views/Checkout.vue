<template>
    <div>
        <!-- <nav class="navbar">
            <a href="#" class="logo">
                <span>Brew Haven</span>
            </a>
        </nav> -->

        <div class="checkout-container">
            <div class="checkout-form">
                <h1 class="form-title">Checkout</h1>

                <div class="form-steps">
                    <!-- <div class="step">Shipping</div>
            <div class="step">Delivery</div>
            <div class="step active">Payment</div> -->
                </div>

                <div class="payment-details">
                    <h2>Your Payment Details</h2>

                    <!-- <form id="payment-form">
                        <div id="payment-element">
                            Stripe.js injects the Payment Element
                        </div>
                        <button id="submit">
                            <div class="spinner hidden" id="spinner"></div>
                            <span id="button-text">Pay now</span>
                        </button>
                        <div id="payment-message" class="hidden"></div>
                    </form>

                    <div id="card-element" class="stripe-element"></div>
                    <div id="card-errors" class="payment-error" v-if="paymentError">{{ paymentError }}</div> -->

                    <div>
                        <div id="payment-element"></div>
                        <!-- <button @click="handlePayment">Pay Now</button> -->
                    </div>



                    <button class="pay-now-btn" @click="handlePayment">PAY NOW</button>
                </div>
            </div>

            <div class="checkout-summary">
                <h2 class="summary-title">Order Summary</h2>

                <div class="order-items">
                    <div class="order-item" v-for="(item, index) in orderItems" :key="index">
                        <div class="item-image">
                            <img :src="item.image" :alt="item.name">
                        </div>
                        <div class="item-details">
                            <h3>{{ item.name }}</h3>
                        </div>
                        <div class="item-price">
                            ${{ item.price.toFixed(2) }}
                        </div>
                    </div>
                </div>

                <!-- <div class="loyalty-section">
                    <div class="loyalty-header">
                        <h3>Loyalty Awards</h3>
                        <span class="help-icon">?</span>
                    </div>
                    <p>We can apply discounts to loyal customers' purchases whether they're visiting in-store, in-app,
                        or online.</p>
                </div> -->

                <div class="summary-line">
                    <span>Subtotal</span>
                    <span>${{ calculateSubtotal().toFixed(2) }}</span>
                </div>

                <!-- <div class="summary-line">
                    <span>Delivery</span>
                    <span>${{ orderSummary.deliveryFee.toFixed(2) }}</span>
                </div> -->

                <div class="summary-line">
                    <span>Taxes</span>
                    <span>${{ calculateTax().toFixed(2) }}</span>
                </div>

                <div class="summary-total">
                    <span>TOTAL</span>
                    <span>${{ calculateTotal().toFixed(2) }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { loadStripe } from '@stripe/stripe-js';

export default {
    data() {
        return {
            stripe: null,
            elements: null,
            clientSecret: null,
            orderItems: [
                { name: "Brew Haven Special Blend", price: 24.99, image: "#" },
                { name: "Artisan Coffee Grinder", price: 89.50, image: "#" }
            ],
            orderSummary: {
                // deliveryFee: 5.00,
                taxRate: 9
            }
        };
    },

    async mounted() {
        await this.initializePayment();
    },

    methods: {
        async initializePayment() {
      try {
        // 1️⃣ Fetch client secret from your backend
        const response = await fetch("http://127.0.0.1:5100/create-payment-intent", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ 
            amount: (this.calculateTotal().toFixed(2) * 100), 
            currency: "sgd" 
        }),
        });

        const data = await response.json();
        console.log("Fetched clientSecret:", data.client_secret);

        if (!data.client_secret) {
          console.error("Error: Missing client secret");
          return;
        }

        this.clientSecret = data.client_secret;

        // 2️⃣ Load Stripe and create elements
        this.stripe = await loadStripe("pk_test_51QwwPAQRYfaBjPIXkJeTKXtIlovCeAoNntY9jRWsAyO3jpq9Kn8f0Y1ne9EJkbX4ic0YE8V9qEIn59UJ6BDiufml004WRnDQed");

        const appearance = {
          theme: "stripe",
        };

        this.elements = this.stripe.elements({ clientSecret: this.clientSecret, appearance });

        // 3️⃣ Create the PaymentElement and mount it
        const paymentElement = this.elements.create("payment");
        paymentElement.mount("#payment-element");

      } catch (error) {
        console.error("Error initializing Stripe:", error);
      }
    },
    async handlePayment() {
      if (!this.stripe || !this.elements) {
        console.error("Stripe not initialized");
        return;
      }

      const { error } = await this.stripe.confirmPayment({
        elements: this.elements,
        confirmParams: {
          return_url: "http://localhost:5173/",
        },
      });

      if (error) {
        console.error("Payment error:", error);
      } else {
        console.log("Payment successful!");
      }
    },
        calculateSubtotal() {
            return this.orderItems.reduce((total, item) => total + item.price, 0);
        },

        calculateTax() {
            return this.calculateSubtotal() * (this.orderSummary.taxRate / 100);
        },

        calculateTotal() {
            return this.calculateSubtotal() + this.calculateTax();
        }
    }
};
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

.navbar {
    background-color: var(--primary);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    display: flex;
    align-items: center;
}

.checkout-container {
    max-width: 1000px;
    margin: 5rem auto 2rem;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr 1fr;
}

.checkout-form {
    padding: 2rem;
}

.form-title {
    font-size: 1.8rem;
    color: var(--primary);
    margin-bottom: 1.5rem;
    font-weight: 600;
}

.form-steps {
    display: flex;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}

.step {
    font-size: 0.9rem;
    color: var(--text-light);
    margin-right: 1.5rem;
    position: relative;
    padding-right: 1.5rem;
}

.step.active {
    color: var(--primary);
    font-weight: 500;
}

.step:not(:last-child)::after {
    content: "›";
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
}

.payment-details {
    margin-top: 1rem;
}

.payment-details h2 {
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    color: var(--primary);
}

.payment-methods {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}

.payment-method {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.8rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: border-color 0.3s;
    gap: 0.5rem;
}

.payment-method.selected {
    border-color: var(--primary);
}

.payment-method img {
    height: 20px;
}

.form-group {
    margin-bottom: 1.2rem;
}

.form-group label {
    display: block;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.form-control {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.input-with-icon {
    position: relative;
}

.input-icon {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
}

.help-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #f0f0f0;
    color: var(--text-light);
    font-size: 0.8rem;
    cursor: pointer;
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
}

.form-row {
    display: flex;
    gap: 1rem;
}

.form-row .form-group {
    flex: 1;
}

.stripe-element {
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 1.5rem;
}

.payment-error {
    color: #cc0000;
    font-size: 0.9rem;
    margin: -0.5rem 0 1.5rem;
}

.security-note {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: var(--text-light);
    margin-bottom: 1rem;
}

.pay-now-btn {
    width: 100%;
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 1rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.pay-now-btn:hover {
    background-color: var(--dark);
}

.checkout-summary {
    background-color: #f8f8f8;
    padding: 2rem;
    border-left: 1px solid #eee;
}

.summary-title {
    font-size: 1.5rem;
    color: var(--primary);
    margin-bottom: 1.5rem;
    font-weight: 600;
}

.order-items {
    margin-bottom: 2rem;
}

.order-item {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}

.item-image {
    width: 60px;
    height: 60px;
    background-color: #fff;
    border-radius: 4px;
    overflow: hidden;
    margin-right: 1rem;
}

.item-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.item-details {
    flex: 1;
}

.item-details h3 {
    font-size: 1rem;
    margin-bottom: 0.2rem;
}

.item-price {
    font-weight: 600;
    font-size: 1rem;
}

.loyalty-section {
    background-color: #f0f0f0;
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
}

.loyalty-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.loyalty-header h3 {
    font-size: 1rem;
    font-weight: 500;
}

.loyalty-section p {
    font-size: 0.8rem;
    color: var(--text-light);
}

.summary-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.8rem;
    font-size: 0.95rem;
}

.summary-total {
    display: flex;
    justify-content: space-between;
    padding-top: 1rem;
    margin-top: 1rem;
    border-top: 1px solid #ddd;
    font-weight: 600;
    font-size: 1.2rem;
}

@media (max-width: 768px) {
    .checkout-container {
        grid-template-columns: 1fr;
        margin-top: 4rem;
    }

    .checkout-summary {
        border-left: none;
        border-top: 1px solid #eee;
    }

    .form-row {
        flex-direction: column;
        gap: 0;
    }

    .payment-methods {
        flex-wrap: wrap;
    }
}
</style>