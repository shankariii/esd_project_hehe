<template>
    <div>
        <div class="checkout-container">
            <div class="checkout-form">
                <h1 class="form-title">Checkout</h1>

                <div class="payment-details">
                    <h2>Your Payment Details</h2>

                    <div>
                        <div id="payment-element"></div>
                    </div>

                    <button class="pay-now-btn" @click="handlePayment">PAY NOW</button>
                </div>
            </div>

            <div class="checkout-summary">
                <h2 class="summary-title">Order Summary</h2>

                <div class="order-items">
                    <div class="order-item" v-for="(item, index) in cartItems" :key="index">
                        <div class="item-image">
                            <img :src="item.image" :alt="item.name">
                        </div>
                        <div class="item-details">
                            <h3>{{ item.name }}</h3>
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
                        </div>
                        <div class="item-price">
                            ${{ (item.price * item.quantity).toFixed(2) }}
                            <div style="font-size: 0.8rem; color: var(--text-light);">
                                {{ item.quantity }} × ${{ item.price.toFixed(2) }}
                            </div>
                        </div>
                    </div>
                </div>

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
</template>

<script>
import { loadStripe } from '@stripe/stripe-js';
import axios from 'axios';

export default {
    data() {
        return {
            stripe: null,
            elements: null,
            clientSecret: null,
            cartItems: [],
            loading: true,
            userId: 'test24', // Replace with dynamic user ID if needed
            outletId: '24',   // Replace with dynamic outlet ID if needed
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

    computed: {
        subtotal() {
            return this.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        },
        tax() {
            return this.subtotal * 0.08; // 8% tax rate
        },
        total() {
            return this.subtotal + this.tax;
        }
    },

    async mounted() {
        await this.fetchCartDetails();
        await this.initializePayment();
    },

    methods: {
        async fetchCartDetails() {
            try {
                this.loading = true;
                console.log('Starting cart data fetch...');

                // Create axios instances with different configurations
                const cartClient = axios.create({
                    baseURL: this.apiConfig.cartService.baseURL,
                    timeout: this.apiConfig.cartService.timeout
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
                console.log('Cart response:', cartResponse.data);

                if (!cartResponse.data?.data?.items) {
                    console.warn('No items found in cart');
                    this.cartItems = [];
                    return;
                }

                // 2. Process each cart item
                this.cartItems = await this.processCartItems(cartResponse.data.data.items, drinkClient, customClient);
                console.log(this.cartItems);

            } catch (error) {
                console.error('Error in fetchCartDetails:', this.formatAxiosError(error));
                alert('Failed to load cart. Please try again later.');
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
                        customizations = customizationResponses.map(r => ({
                            id: r.data.customisation_id,
                            name: r.data.name,
                            price_diff: r.data.price_diff
                        })).sort((a, b) => a.id - b.id);;
                    }

                    processedItems.push({
                        id: item.drink_id,
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
                    // Continue with next item even if one fails
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

        async initializePayment() {
            try {
                // 1️⃣ Fetch client secret from your backend
                const response = await fetch("http://127.0.0.1:5100/create-payment-intent", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ 
                        amount: (this.total * 100), // Convert to cents
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
                    return_url: "http://localhost:5174/",
                },
            });

            if (error) {
                console.error("Payment error:", error);
            } else {
                console.log("Payment successful!");
            }
        }
    }
};
</script>

<style scoped>
/* Your existing styles remain the same */
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