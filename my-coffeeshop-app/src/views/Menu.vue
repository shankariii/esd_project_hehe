<script setup>
import { ref } from 'vue'
import { computed } from 'vue'
import { watch } from 'vue'


const selectedCategory = ref('Hot Coffee');
const selectedItem = ref(null);
const customization = ref({
    size: 'Medium',
    milk: 'Whole Milk',
    extras: []
});
const cart = ref([]);
const showCart = ref(false);
const mobileMenuOpen = ref(false);

// DOM refs for Bootstrap modals
const customizeModal = ref(null);
const cartModal = ref(null);
let bsCustomizeModal = null;
let bsCartModal = null;

// Menu data
// const categories = ['Hot Coffee', 'Iced Coffee', 'Tea', 'Pastries'];

const menuItems = [
    {
        id: 1,
        name: 'Espresso',
        category: 'Hot Coffee',
        description: 'Strong and concentrated coffee served in a small cup',
        basePrice: 2.50
    },
    {
        id: 2,
        name: 'Cappuccino',
        category: 'Hot Coffee',
        description: 'Equal parts espresso, steamed milk, and milk foam',
        basePrice: 3.75
    },
    {
        id: 3,
        name: 'Latte',
        category: 'Hot Coffee',
        description: 'Espresso with steamed milk and a light layer of foam',
        basePrice: 4.25
    },
    {
        id: 4,
        name: 'Iced Latte',
        category: 'Iced Coffee',
        description: 'Espresso and milk served over ice',
        basePrice: 4.50
    },
    {
        id: 5,
        name: 'Cold Brew',
        category: 'Iced Coffee',
        description: 'Coffee brewed with cold water over 12+ hours',
        basePrice: 4.75
    },
    {
        id: 6,
        name: 'Green Tea',
        category: 'Tea',
        description: 'Refreshing tea with antioxidant properties',
        basePrice: 3.25
    },
    {
        id: 7,
        name: 'Earl Grey',
        category: 'Tea',
        description: 'Black tea flavored with oil of bergamot',
        basePrice: 3.25
    },
    {
        id: 8,
        name: 'Croissant',
        category: 'Pastries',
        description: 'Buttery, flaky pastry of French origin',
        basePrice: 3.50
    },
    {
        id: 9,
        name: 'Blueberry Muffin',
        category: 'Pastries',
        description: 'Moist muffin filled with fresh blueberries',
        basePrice: 3.75
    }
];

// Customization options
const sizes = [
    { name: 'Small', priceDiff: 0 },
    { name: 'Medium', priceDiff: 0.50 },
    { name: 'Large', priceDiff: 0.75 }
];

const milkOptions = [
    { name: 'Whole Milk', priceDiff: 0 },
    { name: 'Skim Milk', priceDiff: 0 },
    { name: 'Almond Milk', priceDiff: 0.75 },
    { name: 'Oat Milk', priceDiff: 0.75 },
    { name: 'Soy Milk', priceDiff: 0.75 }
];

const extras = [
    { name: 'Extra Shot', price: 1.00 },
    { name: 'Vanilla Syrup', price: 0.75 },
    { name: 'Caramel Syrup', price: 0.75 },
    { name: 'Whipped Cream', price: 0.50 },
    { name: 'Chocolate Drizzle', price: 0.50 }
];

// Computed
const filteredItems = computed(() => {
    return menuItems.filter(item => item.category === selectedCategory.value);
});

// Initialize Bootstrap modals after component is mounted
const initModals = () => {
    bsCustomizeModal = new bootstrap.Modal(customizeModal.value);
    bsCartModal = new bootstrap.Modal(cartModal.value);
};

// Watch for showCart changes to show/hide the cart modal
watch(showCart, (newVal) => {
    if (newVal) {
        bsCartModal.show();
    } else {
        bsCartModal.hide();
    }
});

// Methods
const toggleMenu = () => {
    mobileMenuOpen.value = !mobileMenuOpen.value;
};

const openCustomizeModal = (item) => {
    selectedItem.value = item;
    // Reset customization for new item
    customization.value = {
        size: 'Small',
        milk: 'Whole Milk',
        extras: [],
        quantity: 1
    };
    bsCustomizeModal.show();
};

const closeCustomizeModal = () => {
    bsCustomizeModal.hide();
};

const selectSize = (size) => {
    customization.value.size = size;
};

const selectMilk = (milk) => {
    customization.value.milk = milk;
};

const toggleExtra = (extra) => {
    const extras = customization.value.extras;
    const index = extras.indexOf(extra);

    if (index === -1) {
        extras.push(extra);
    } else {
        extras.splice(index, 1);
    }
};

function incrementQuantity() {
    customization.value.quantity++;
}

function decrementQuantity() {
    if (customization.value.quantity > 1) {
        customization.value.quantity--;
    }
}

const calculateTotalPrice = () => {
    if (!selectedItem.value) return 0;

    let total = selectedItem.value.basePrice;

    // Add size price difference
    const selectedSizeObj = sizes.find(s => s.name === customization.value.size);
    if (selectedSizeObj) {
        total += selectedSizeObj.priceDiff;
    }

    // Add milk price difference
    const selectedMilkObj = milkOptions.find(m => m.name === customization.value.milk);
    if (selectedMilkObj) {
        total += selectedMilkObj.priceDiff;
    }

    // Add extras
    customization.value.extras.forEach(extra => {
        const extraObj = extras.find(e => e.name === extra);
        if (extraObj) {
            total += extraObj.price;
        }
    });

    total *= customization.value.quantity;

    return total;
};

const addToCart = () => {
    cart.value.push({
        id: selectedItem.value.id,
        name: selectedItem.value.name,
        customization: JSON.parse(JSON.stringify(customization.value)),
        price: calculateTotalPrice(),
        quantity: 1
    });

    closeCustomizeModal();
    showCart.value = true;
};

const removeFromCart = (index) => {
    cart.value.splice(index, 1);
};

const updateQuantity = (index, change) => {
    const newQuantity = cart.value[index].quantity + change;
    if (newQuantity > 0) {
        cart.value[index].quantity = newQuantity;
    }
};

const calculateCartTotal = () => {
    return cart.value.reduce((total, item) => {
        return total + (item.price * item.quantity);
    }, 0);
};

const checkout = () => {
    alert('Thank you for your order! Your total is $' + calculateCartTotal().toFixed(2));
    cart.value = [];
    showCart.value = false;
};
</script>

<template>
    <!-- Menu Items -->
    <div class="row g-4">
        <div class="col-md-4 col-sm-6" v-for="item in filteredItems" :key="item.id">
            <div class="card h-100 menu-card" @click="openCustomizeModal(item)">
                <img :src="`/api/placeholder/400/200?text=${item.name}`" class="card-img-top" :alt="item.name">
                <div class="card-body">
                    <h5 class="card-title">{{ item.name }}</h5>
                    <p class="card-text text-muted">{{ item.description }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="fs-5">${{ item.basePrice.toFixed(2) }}</span>
                        <button class="btn btn-primary btn-sm">Order</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Customization Page -->
    <div class="modal fade" id="customizeModal" tabindex="-1" ref="customizeModal">
        <div class="modal-dialog modal-lg">
            <div class="modal-content" v-if="selectedItem">
                <div class="modal-header">
                    <h5 class="modal-title">Customize Your {{ selectedItem.name }}</h5>
                    <button type="button" class="btn-close" @click="closeCustomizeModal"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div id="prodDesc" class="d-flex align-items-center justify-content-between">
                            <div>
                                <h3>About this drink</h3>
                                <p>{{ selectedItem.description }}</p>
                            </div>
                            <img style="width: 200px;" src="../images/espresso.avif" class="img-fluid rounded"
                                alt="selectedItem.name">
                        </div>
                        <div>
                            <!-- Size Selection -->
                            <div class="mb-4">
                                <h5>Size</h5>
                                <div class="d-flex justify-content-between mt-3">
                                    <div v-for="size in sizes" :key="size.name"
                                        class="size-option d-flex flex-column align-items-center"
                                        :class="{ selected: customization.size === size.name }"
                                        @click="selectSize(size.name)">
                                        <div class="fs-6">{{ size.name }}</div>
                                        <small>(+${{ size.priceDiff.toFixed(2) }})</small>
                                    </div>
                                </div>
                            </div>

                            <!-- Milk Options -->
                            <div class="mb-4">
                                <h5>Milk</h5>
                                <div class="options">
                                    <button v-for="milk in milkOptions" :key="milk.name" class="option-btn"
                                        :class="{ selected: customization.milk === milk.name }"
                                        @click="selectMilk(milk.name)">
                                        <!-- {{milk.name}} <span v-if="milk.priceDiff > 0"> (+${{ milk.priceDiff.toFixed(2) }}) -->
                                        {{ milk.name }} {{ milk.priceDiff > 0 ? `(+$${milk.priceDiff.toFixed(2)})` : ''
                                        }}
                                    </button>
                                </div>
                            </div>

                            <!-- Extras -->
                            <div class="mb-4">
                                <h5>Extras</h5>
                                <div class="options">
                                    <button v-for="extra in extras" :key="extra.name" class="option-btn"
                                        :class="{ selected: customization.extras.includes(extra.name) }"
                                        @click="toggleExtra(extra.name)">
                                        {{ extra.name }} {{ extra.price > 0 ? `(+$${extra.price.toFixed(2)})` : '' }}
                                    </button>
                                </div>
                            </div>

                            <div class="option-group">
                                <h5>Quantity</h5>
                                <div class="quantity-control">
                                    <button class="quantity-btn" @click="decrementQuantity">-</button>
                                    <span class="quantity-display">{{ customization.quantity }}</span>
                                    <button class="quantity-btn" @click="incrementQuantity">+</button>
                                </div>
                            </div>

                            <!-- Total Price -->
                            <div>
                                <div class="d-flex justify-content-between align-items-center">
                                    <span class="fw-bold">Total Price:</span>
                                    <span class="fs-4" style="color: var(--primary);">${{
                                        calculateTotalPrice().toFixed(2) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer d-flex align-items-center" style="gap: 1rem; margin-top: 1rem;">
                    <button type="button" class="checkout-btn"
                        style="background-color: #9e9e9e; width: auto; padding: 0.375rem 0.75rem;"
                        @click="closeCustomizeModal">Cancel</button>
                    <button type="button" class="checkout-btn" style="width: auto; padding: 0.375rem 0.75rem;"
                        @click="addToCart">Add to Cart</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Cart Modal -->
    <div class="modal fade" id="cartModal" tabindex="-1" ref="cartModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Your Cart</h5>
                    <button type="button" class="btn-close" @click="showCart = false"></button>
                </div>
                <div class="modal-body">
                    <div v-if="cart.length === 0" class="text-center py-5">
                        <p class="text-muted">Your cart is empty</p>
                        <button class="btn btn-outline-primary mt-3" @click="showCart = false">
                            Browse Menu
                        </button>
                    </div>
                    <div v-else>
                        <div v-for="(item, index) in cart" :key="index" class="card mb-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between">
                                    <h5 class="card-title">{{ item.name }}</h5>
                                    <button class="btn btn-sm btn-outline-danger" @click="removeFromCart(index)">
                                        <span>&times;</span>
                                    </button>
                                </div>
                                <p class="card-text text-muted mb-2">
                                    Size: {{ item.customization.size }}
                                    <br>
                                    Milk: {{ item.customization.milk }}
                                    <span v-if="item.customization.extras.length > 0">
                                        <br>
                                        Extras: {{ item.customization.extras.join(', ') }}
                                    </span>
                                </p>
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <button class="btn btn-sm btn-outline-secondary"
                                            @click="updateQuantity(index, -1)" :disabled="item.quantity <= 1">−</button>
                                        <span class="mx-2">{{ item.quantity }}</span>
                                        <button class="btn btn-sm btn-outline-secondary"
                                            @click="updateQuantity(index, 1)">+</button>
                                    </div>
                                    <span class="fw-bold">${{ (item.price * item.quantity).toFixed(2) }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="alert alert-info mt-4">
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="fw-bold">Subtotal:</span>
                                <span class="fs-5">${{ calculateCartTotal().toFixed(2) }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="showCart = false">
                        Continue Shopping
                    </button>
                    <button type="button" class="btn btn-success" :disabled="cart.length === 0" @click="checkout">
                        Checkout
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
/* Menu Card Styles */
.menu-card {
    transition: transform 0.3s;
    cursor: pointer;
}

.menu-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-img-top {
    height: 200px;
    object-fit: cover;
}

.cart-badge {
    position: relative;
    top: -8px;
    right: 5px;
}

.custom-option {
    cursor: pointer;
    padding: 8px;
    border-radius: 4px;
    margin: 5px 0;
}

.custom-option:hover {
    background-color: var(--primary);
}

.custom-option.selected {
    background-color: var(--secondary);
    border: 1px solid var(--dark);
}

.size-option {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 5px;
    border-radius: 50%;
    cursor: pointer;
    background-color: var(--accent);
    color: black;
}

.size-option.selected {
    background-color: var(--primary);
    border: 2px solid;
    color: white;
}

.option {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.option-group {
    margin-bottom: 1.5rem;
}

.option-btn {
    background-color: var(--accent);
    border: none;
    padding: 0.5rem 1rem;
    margin: 5px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
}

.option-btn.selected {
    background-color: var(--primary);
    color: white;
}

.quantity-control {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.quantity-btn {
    background-color: var(--accent);
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    font-weight: bold;
    cursor: pointer;
}

.quantity-display {
    font-size: 1.2rem;
    font-weight: bold;
}

.cart-total {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    font-size: 1.2rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 2px solid var(--accent);
}

.checkout-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 4px;
    font-size: 1.1rem;
    margin-top: 1rem;
    width: 100%;
    cursor: pointer;
    transition: background-color 0.3s;
}

.checkout-btn:hover {
    background-color: var(--secondary);
}
</style>