<template>
    <div class="track-order-container">
        <!-- Loading state -->
        <div v-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading your order details...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="error-state">
            <p>Error: {{ error }}</p>
            <button class="btn" @click="goBack">Go Back</button>
        </div>

        <!-- Order Status Container -->
        <div v-else class="order-details-container">
            <div class="order-header">
                <h1>Track Your Order</h1>
                <div class="order-id">Order #{{ orderId }}</div>
                <div class="order-date">{{ formatDate(order.date) }}</div>
                <div class="estimated-time">
                    Estimated delivery: {{ formatTime(estimatedDeliveryTime) }}
                </div>
            </div>

            <!-- Order Status -->
            <div class="status-container">
                <div class="status-title">Order Status</div>

                <div class="status-timeline">
                    <div class="status-step" :class="{ 'completed': statusSteps.orderPlaced.completed }">
                        <div class="step-icon">
                            <span v-if="statusSteps.orderPlaced.completed">✓</span>
                            <span v-else>1</span>
                        </div>
                        <div class="step-details">
                            <div class="step-name">Order Placed</div>
                            <div class="step-time" v-if="statusSteps.orderPlaced.timestamp">
                                {{ formatTime(statusSteps.orderPlaced.timestamp) }}
                            </div>
                        </div>
                    </div>

                    <div class="status-step" :class="{ 'completed': statusSteps.preparing.completed }">
                        <div class="step-icon">
                            <span v-if="statusSteps.preparing.completed">✓</span>
                            <span v-else>2</span>
                        </div>
                        <div class="step-details">
                            <div class="step-name">Preparing</div>
                            <div class="step-time" v-if="statusSteps.preparing.timestamp">
                                {{ formatTime(statusSteps.preparing.timestamp) }}
                            </div>
                        </div>
                    </div>

                    <div class="status-step" :class="{ 'completed': statusSteps.readyForPickup.completed }">
                        <div class="step-icon">
                            <span v-if="statusSteps.readyForPickup.completed">✓</span>
                            <span v-else>3</span>
                        </div>
                        <div class="step-details">
                            <div class="step-name">Ready for Pickup</div>
                            <div class="step-time" v-if="statusSteps.readyForPickup.timestamp">
                                {{ formatTime(statusSteps.readyForPickup.timestamp) }}
                            </div>
                        </div>
                    </div>

                    <div class="status-step" :class="{ 'completed': statusSteps.completed.completed }">
                        <div class="step-icon">
                            <span v-if="statusSteps.completed.completed">✓</span>
                            <span v-else>4</span>
                        </div>
                        <div class="step-details">
                            <div class="step-name">Completed</div>
                            <div class="step-time" v-if="statusSteps.completed.timestamp">
                                {{ formatTime(statusSteps.completed.timestamp) }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Order Items -->
            <div class="order-items-container">
                <div class="section-title">Order Details</div>
                <div class="order-items">
                    <div v-for="(item, index) in order.items" :key="index" class="order-item">
                        <div class="item-quantity">{{ item.quantity }}x</div>
                        <div class="item-name">{{ item.name }}</div>
                        <div class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</div>
                    </div>
                </div>
                <div class="order-total">
                    <span>Total:</span>
                    <span>${{ order.total.toFixed(2) }}</span>
                </div>
            </div>

            <!-- Map Section -->
            <div class="map-container">
                <div class="section-title">Outlet Location</div>
                <div class="map" ref="mapContainer" style="height: 400px; width: 100%;"></div>

                <div class="outlet-info">
                    <div class="outlet-name">{{ outlet.name }}</div>
                    <div class="outlet-address">{{ outlet.address }}</div>
                    <div class="outlet-contact">
                        <a :href="`tel:${outlet.phone}`">{{ outlet.phone }}</a>
                    </div>
                </div>

                <button class="btn" @click="getDirections">Get Directions</button>
            </div>

            <div class="actions">
                <button class="btn btn-secondary" @click="goBack">Back to Profile</button>
                <button class="btn" @click="contactSupport">Contact Support</button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
    name: 'TrackOrder',
    setup() {
        const route = useRoute();
        const router = useRouter();
        const orderId = ref(route.params.orderId);
        const isLoading = ref(true);
        const error = ref(null);
        const mapContainer = ref(null);
        const map = ref(null);
        const mapInitialized = ref(false);
        const directionsService = ref(null);
        const directionsRenderer = ref(null);

        // Order data (replace with real API call)
        const order = ref({
            id: orderId.value,
            date: '2025-04-02T15:30:00Z',
            status: 'Preparing',
            items: [
                { name: 'Cappuccino (Large)', price: 4.99, quantity: 2 },
                { name: 'Chocolate Croissant', price: 3.50, quantity: 1 }
            ],
            total: 13.48
        });

        // Outlet data (replace with real data)
        const outlet = ref({
            name: 'Coffee Break Downtown',
            address: '123 Main Street, New York, NY 10001',
            phone: '(555) 123-4567',
            location: { lat: 40.712776, lng: -74.005974 } // NYC coordinates
        });

        // Status steps with timestamps
        const statusSteps = ref({
            orderPlaced: {
                completed: true,
                timestamp: new Date('2025-04-02T15:30:00Z')
            },
            preparing: {
                completed: true,
                timestamp: new Date('2025-04-02T15:35:00Z')
            },
            readyForPickup: {
                completed: false,
                timestamp: null
            },
            completed: {
                completed: false,
                timestamp: null
            }
        });

        // Estimated delivery time (10 minutes from now)
        const estimatedDeliveryTime = ref(new Date(new Date().getTime() + 10 * 60000));

        // Format date for display
        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            }).format(date);
        };

        // Format time for display
        const formatTime = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('en-US', {
                hour: 'numeric',
                minute: 'numeric',
                hour12: true
            }).format(date);
        };

        // Initialize Google Maps
        const initializeMap = () => {
            if (!window.google || mapInitialized.value) return;

            if (!mapContainer.value) {
                console.error('Map container element not found');
                error.value = 'Could not load the map';
                return;
            }

            try {
                // Create map
                map.value = new window.google.maps.Map(mapContainer.value, {
                    center: outlet.value.location,
                    zoom: 15,
                    mapTypeControl: false
                });

                // Add marker for outlet
                new window.google.maps.Marker({
                    position: outlet.value.location,
                    map: map.value,
                    title: outlet.value.name
                });

                // Initialize directions services
                directionsService.value = new window.google.maps.DirectionsService();
                directionsRenderer.value = new window.google.maps.DirectionsRenderer({
                    map: map.value,
                    suppressMarkers: false
                });

                mapInitialized.value = true;
            } catch (e) {
                console.error('Error initializing map:', e);
                error.value = 'Could not load the map';
            }
        };

        // Load Google Maps API
        const loadGoogleMapsAPI = () => {
            if (window.google && window.google.maps) {
                initializeMap();
                return;
            }

            const script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDyzGN00mpIu7qElBpIFwiPjWyQlkIfHHM&callback=initMap`;
            script.async = true;
            script.defer = true;

            window.initMap = () => {
                initializeMap();
            };

            document.head.appendChild(script);
        };

        // Get directions to the outlet
        const getDirections = () => {
            if (!mapInitialized.value || !directionsService.value) {
                alert('Map is not initialized yet. Please try again in a moment.');
                return;
            }

            // Try to get user's location
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const origin = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };

                        directionsService.value.route(
                            {
                                origin: origin,
                                destination: outlet.value.location,
                                travelMode: 'DRIVING'
                            },
                            (response, status) => {
                                if (status === 'OK') {
                                    directionsRenderer.value.setDirections(response);
                                } else {
                                    alert('Could not calculate directions: ' + status);
                                }
                            }
                        );
                    },
                    () => {
                        alert('Unable to get your location. Please enable location services.');
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        };

        // Simulated data loading
        const loadOrderData = () => {
            isLoading.value = true;

            // Simulate API call with timeout
            setTimeout(() => {
                // Data would normally come from an API
                isLoading.value = false;
            }, 1500);
        };

        // Navigation functions
        const goBack = () => {
            router.push('/profile');
        };

        const contactSupport = () => {
            alert('Support contact feature will be implemented soon.');
        };

        onMounted(() => {
            loadOrderData();
            loadGoogleMapsAPI();
            
        });

        return {
            orderId,
            isLoading,
            error,
            order,
            outlet,
            mapContainer,
            statusSteps,
            estimatedDeliveryTime,
            formatDate,
            formatTime,
            getDirections,
            goBack,
            contactSupport
        };
    }
};
</script>

<style scoped>
.track-order-container {
    max-width: 1000px;
    margin: 6rem auto;
    padding: 0 1.5rem;
}

/* Loading State */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Error State */
.error-state {
    text-align: center;
    padding: 3rem;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

/* Order Details Container */
.order-details-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    padding: 2rem;
}

.order-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--light);
}

.order-header h1 {
    font-size: 2rem;
    color: var(--primary);
    margin-bottom: 0.5rem;
}

.order-id {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.order-date {
    color: var(--text-light);
    margin-bottom: 0.5rem;
}

.estimated-time {
    font-weight: bold;
    color: var(--primary);
    font-size: 1.1rem;
}

/* Status Section */
.status-container {
    margin-bottom: 2rem;
}

.status-title,
.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    color: var(--dark);
}

.status-timeline {
    display: flex;
    justify-content: space-between;
    position: relative;
    margin-bottom: 2rem;
}

.status-timeline::before {
    content: '';
    position: absolute;
    height: 4px;
    background-color: var(--light);
    top: 25px;
    left: 40px;
    right: 40px;
    z-index: 1;
}

.status-step {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 25%;
}

.step-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: white;
    border: 3px solid var(--light);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--text-light);
}

.status-step.completed .step-icon {
    background-color: var(--primary);
    border-color: var(--primary);
    color: white;
}

.step-details {
    text-align: center;
}

.step-name {
    font-weight: bold;
    margin-bottom: 0.2rem;
}

.step-time {
    font-size: 0.8rem;
    color: var(--text-light);
}

/* Order Items */
.order-items-container {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--light);
}

.order-items {
    margin-bottom: 1rem;
}

.order-item {
    display: flex;
    margin-bottom: 0.8rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--light);
}

.item-quantity {
    width: 40px;
    font-weight: bold;
}

.item-name {
    flex: 1;
}

.item-price {
    font-weight: bold;
    color: var(--dark);
}

.order-total {
    display: flex;
    justify-content: space-between;
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--primary);
    padding-top: 1rem;
}

/* Map Container */
.map-container {
    margin-bottom: 2rem;
}

.map {
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

.outlet-info {
    background-color: var(--light);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.outlet-name {
    font-weight: bold;
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}

.outlet-address {
    margin-bottom: 0.3rem;
    color: var(--text);
}

.outlet-contact a {
    color: var(--primary);
    text-decoration: none;
}

/* Action Buttons */
.actions {
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
}

.btn {
    padding: 0.8rem 1.5rem;
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 500;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: var(--dark);
}

.btn-secondary {
    background-color: var(--light);
    color: var(--text);
    border: 1px solid var(--secondary);
}

.btn-secondary:hover {
    background-color: var(--secondary);
    color: white;
}

@media (max-width: 768px) {
    .status-timeline {
        flex-direction: column;
    }

    .status-timeline::before {
        height: calc(100% - 80px);
        width: 4px;
        top: 25px;
        left: 23px;
        right: auto;
    }

    .status-step {
        flex-direction: row;
        width: 100%;
        margin-bottom: 1.5rem;
        align-items: flex-start;
    }

    .step-icon {
        margin-right: 1rem;
        margin-bottom: 0;
    }

    .step-details {
        text-align: left;
    }

    .actions {
        flex-direction: column;
        gap: 1rem;
    }

    .btn {
        width: 100%;
    }
}
</style>