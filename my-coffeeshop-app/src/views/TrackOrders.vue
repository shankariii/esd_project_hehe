<template>
    <div class="track-order-container">
        <!-- Loading state -->
        <div v-if="isLoading" class="loading-state">
            Loading order details...
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="error-state">
            Error: {{ error }}
        </div>

        <!-- Main content -->
        <div v-else class="order-details">

            <router-link to="/profile" class="back-link">
                &larr; Back to Profile
            </router-link>
            <div class="order-header">
                <h1 style="margin-top: 20px;">Track Your Order</h1>
            </div>

            <!-- Horizontal Status Timeline at the top -->
            <div class="horizontal-timeline">
                <div class="timeline-container">
                    <div v-for="(step, index) in statusSteps" :key="index" class="timeline-step"
                        :class="{ 'active': step.active, 'completed': step.completed }">
                        <div class="timeline-marker">
                            <span v-if="step.completed" class="checkmark">✓</span>
                        </div>
                        <div class="timeline-content">
                            <div class="timeline-title">{{ step.title }}</div>
                            <div class="timeline-time" v-if="step.time">{{ step.time }}</div>
                        </div>
                        <div v-if="index < statusSteps.length - 1" class="timeline-connector"></div>
                    </div>
                </div>
            </div>

            <div class="order-info">
                <div class="order-summary">
                    <h2>Order #{{ order.id }}</h2>
                    <div class="status-badge" :class="statusClass">
                        {{ order.status }}
                    </div>

                    <div class="info-grid">
                        <div class="info-item">
                            <span class="label">Order Date:</span>
                            <span class="value">{{ formatDate(order.date) }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Outlet:</span>
                            <span class="value">{{ order.outletName }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Outlet Address:</span>
                            <span class="value">{{ order.outletAddress }}</span>
                        </div>
                        <div class="info-item">
                            <span class="label">Estimated Delivery:</span>
                            <span class="value">{{ estimatedDelivery }}</span>
                        </div>
                    </div>

                    <div class="order-items">
                        <h3>Your Items</h3>
                        <div v-for="(item, index) in order.items" :key="index" class="item">
                            <span class="quantity">{{ item.quantity }}x</span>
                            <span class="name">{{ item.name }}</span>
                            <span class="price">${{ item.price.toFixed(2) }}</span>
                        </div>
                        <div class="total">
                            <span>Total:</span>
                            <span>${{ order.total.toFixed(2) }}</span>
                        </div>
                    </div>
                </div>

                <div class="map-container">
                    <div class="map" ref="map"></div>
                    <div class="directions-panel" ref="directionsPanel"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
    name: 'TrackOrder',
    setup() {
        const route = useRoute();
        const orderId = route.params.orderId;
        const map = ref(null);
        const directionsPanel = ref(null);
        const isLoading = ref(true);
        const error = ref(null);

        // For demo purposes - replace with real data from your backend
        const order = ref({
            id: orderId,
            date: '2025-04-02T15:30:00Z',
            status: 'Processing',
            outletName: 'Downtown Cafe',
            outletAddress: '81 Victoria St, Singapore 188065',
            outletLat: 1.297106,
            outletLng: 103.8498,
            items: [
                { name: 'Product Name', price: 24.99, quantity: 2 },
                { name: 'Another Product', price: 15.99, quantity: 1 }
            ],
            total: 65.97,
            statusHistory: [
                { status: 'Order Placed', time: '2025-04-02T15:30:00Z' },
                { status: 'Preparing', time: '2025-04-02T15:45:00Z' },
                { status: 'Ready for Pickup', time: null },
                { status: 'Completed', time: null }
            ]
        });

        const statusClass = computed(() => {
            return {
                'processing': order.value.status === 'Processing',
                'preparing': order.value.status === 'Preparing',
                'ready': order.value.status === 'Ready for Pickup',
                'completed': order.value.status === 'Completed'
            };
        });

        const estimatedDelivery = computed(() => {
            const date = new Date(order.value.date);
            date.setMinutes(date.getMinutes() + 45); // Add 45 minutes for demo
            return formatTime(date);
        });

        const statusSteps = computed(() => {
            return order.value.statusHistory.map(step => ({
                title: step.status,
                time: step.time ? formatTime(new Date(step.time)) : null,
                active: order.value.status === step.status,
                completed: step.time !== null
            }));
        });

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }).format(date);
        };

        const formatTime = (date) => {
            return new Intl.DateTimeFormat('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            }).format(date);
        };

        const initMap = () => {
            // Load Google Maps API script
            const script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDyzGN00mpIu7qElBpIFwiPjWyQlkIfHHM&libraries=places,geometry,directions`;
            script.async = true;
            script.defer = true;
            script.onload = () => {
                renderMap();
            };
            document.head.appendChild(script);
        };

        const renderMap = () => {
            // For demo, we'll use San Francisco as user location
            // In a real app, you would get this from geolocation API
            const userLocation = { lat: 1.28136, lng: 103.8352 };
            const outletLocation = {
                lat: order.value.outletLat,
                lng: order.value.outletLng
            };

            // Create map
            const mapInstance = new google.maps.Map(map.value, {
                center: userLocation,
                zoom: 13,
                styles: [
                    {
                        featureType: "poi",
                        elementType: "labels",
                        stylers: [{ visibility: "off" }]
                    }
                ]
            });

            // Add markers
            new google.maps.Marker({
                position: userLocation,
                map: mapInstance,
                title: "Your location",
                icon: {
                    url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                }
            });

            new google.maps.Marker({
                position: outletLocation,
                map: mapInstance,
                title: order.value.outletName,
                icon: {
                    url: "https://maps.google.com/mapfiles/ms/icons/red-dot.png"
                }
            });

            // Calculate and display route
            const directionsService = new google.maps.DirectionsService();
            const directionsRenderer = new google.maps.DirectionsRenderer({
                map: mapInstance,
                panel: directionsPanel.value,
                suppressMarkers: true
            });

            directionsService.route(
                {
                    origin: userLocation,
                    destination: outletLocation,
                    travelMode: google.maps.TravelMode.WALKING
                },
                (response, status) => {
                    if (status === "OK") {
                        directionsRenderer.setDirections(response);
                    } else {
                        console.error("Directions request failed due to " + status);
                    }
                }
            );
        };

        onMounted(() => {
            // In a real app, you would fetch order details here
            setTimeout(() => {
                isLoading.value = false;
                initMap();
            }, 1000);
        });

        return {
            isLoading,
            error,
            order,
            statusClass,
            estimatedDelivery,
            statusSteps,
            formatDate,
            formatTime,
            map,
            directionsPanel
        };
    }
};
</script>

<style scoped>
.track-order-container {
    max-width: 1200px;
    margin: 6rem auto;
    padding: 0 2rem;
}

.loading-state,
.error-state {
    text-align: center;
    padding: 3rem;
    font-size: 1.2rem;
}

.error-state {
    color: #d32f2f;
}

.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.order-header h1 {
    font-size: 2rem;
    color: var(--primary);
}

.back-link {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    display: flex;
    align-items: center;
}

.back-link:hover {
    text-decoration: underline;
}

.order-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 3rem;
}

.order-summary {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.order-summary h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--dark);
}

.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-weight: 600;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    text-transform: uppercase;
}

.status-badge.processing {
    background-color: #fef7e0;
    color: var(--accent);
}

.status-badge.preparing {
    background-color: #e8f0fe;
    color: #1a73e8;
}

.status-badge.ready {
    background-color: #e6f4ea;
    color: #34a853;
}

.status-badge.completed {
    background-color: #f6f6f6;
    color: #5f6368;
}

.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.info-item {
    display: flex;
    flex-direction: column;
}

.label {
    font-size: 0.9rem;
    color: var(--text-light);
    margin-bottom: 0.3rem;
}

.value {
    font-weight: 500;
    color: var(--text);
}

.order-items {
    border-top: 1px solid var(--light);
    padding-top: 1.5rem;
}

.order-items h3 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: var(--dark);
}

.item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.8rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #f0f0f0;
}

.quantity {
    font-weight: 500;
    color: var(--primary);
    min-width: 30px;
}

.name {
    flex-grow: 1;
    margin: 0 1rem;
}

.price {
    font-weight: 500;
    color: var(--text);
}

.total {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
    font-weight: bold;
    font-size: 1.1rem;
    color: var(--primary);
}

.map-container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.map {
    height: 400px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
}

.directions-panel {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    max-height: 200px;
    overflow-y: auto;
}

/* Horizontal Timeline Styles */
.horizontal-timeline {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
}

.timeline-container {
    display: flex;
    justify-content: space-between;
    position: relative;
    padding: 0 1rem;
}

.timeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    flex: 1;
    z-index: 1;
}

.timeline-marker {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: #e0e0e0;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.5rem;
    position: relative;
    border: 2px solid white;
}

.timeline-step.completed .timeline-marker {
    background: var(--primary);
    color: white;
}

.timeline-step.active .timeline-marker {
    background: var(--primary);
    color: white;
    box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.2);
}

.timeline-content {
    text-align: center;
    max-width: 100px;
}

.timeline-title {
    font-weight: 500;
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
    word-break: break-word;
}

.timeline-step.completed .timeline-title {
    color: var(--text);
}

.timeline-step.active .timeline-title {
    color: var(--primary);
    font-weight: 600;
}

.timeline-time {
    font-size: 0.8rem;
    color: var(--text-light);
}

.timeline-connector {
    position: absolute;
    top: 1rem;
    left: 50%;
    right: -50%;
    height: 2px;
    background: #e0e0e0;
    z-index: -1;
}

.timeline-step.completed .timeline-connector {
    background: var(--primary);
}

.checkmark {
    font-size: 0.9rem;
}

@media (max-width: 768px) {
    .order-info {
        grid-template-columns: 1fr;
    }

    .order-summary {
        order: 2;
    }

    .map-container {
        order: 1;
    }

    .timeline-container {
        flex-wrap: wrap;
        justify-content: flex-start;
        gap: 1rem;
    }

    .timeline-step {
        flex: 0 0 calc(50% - 0.5rem);
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .timeline-content {
        text-align: left;
        max-width: none;
        margin-left: 0.5rem;
    }

    .timeline-connector {
        display: none;
    }
}
</style>