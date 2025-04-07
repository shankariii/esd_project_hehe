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
  
        <div class="order-info">
          <div class="order-summary">
            <h2>Order #{{ orderId }}</h2>
            <div class="status-badge" :class="statusClass">
              {{ order.status }}
            </div>
  
            <div class="info-grid">
              <div class="info-item">
                <span class="label">Order Date:</span>
                <span class="value">{{ formatDate(order.date_created) }}</span>
              </div>
              <div class="info-item">
                <span class="label">Outlet:</span>
                <span class="value">{{ order.outlet_name.name }}</span>
              </div>
              <div class="info-item">
                <span class="label">Outlet Address:</span>
                <span class="value">{{ order.outlet_name.address }}</span>
              </div>
              <div class="info-item">
                <span class="label">Estimated Delivery:</span>
                <span class="value">{{ estimatedDelivery }}</span>
              </div>
            </div>
  
            <div class="order-items">
              <h3>Your Items</h3>
              <div v-for="(item, index) in order.items" :key="index" class="item">
                <div class="item-main">
                  <span class="quantity">{{ item.quantity }}x</span>
                  <span class="name">{{ item.drink_name }}</span>
                  <span class="price">${{ item.drink_price.toFixed(2) }}</span>
                </div>
                <!-- Show customizations if they exist -->
                <div v-if="item.customizations && item.customizations.length > 0" class="customizations">
                  <div v-for="(customization, i) in item.customizations" :key="i" class="customization-item">
                    <span class="customization-name">{{ customization.name || customization.type }}:</span>
                    <span class="customization-value">{{ customization.value || customization.option }}</span>
                    <span v-if="customization.price" class="customization-price">
                      +${{ customization.price.toFixed(2) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="total">
                <span>Total:</span>
                <span>${{ order.total_price.toFixed(2) }}</span>
              </div>
            </div>
  
            <!-- Order confirmation button if status is "Ready for Pickup" -->
            <div v-if="order.status === 'ready for pickup'" class="confirm-pickup">
              <p>Your order is ready! Please confirm when you've collected it.</p>
              <button @click="confirmPickup" class="confirm-button">
                Confirm Collection
              </button>
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
  import { useRoute, useRouter } from 'vue-router';
  import { useAuthStore } from '../authStore'; 
  
  export default {
    name: 'TrackOrder',
    setup() {
      const route = useRoute();
      const router = useRouter();
      const authStore = useAuthStore();
      const userId = authStore.user?.uid;
      const orderId = route.params.order_id;
      
      const map = ref(null);
      const directionsPanel = ref(null);
      const isLoading = ref(true);
      const error = ref(null);
      const order = ref(null);
  
      // Helper function to determine status rank for comparison
      const getStatusRank = (status) => {
        const statusRanks = {
          'order placed': 0,
          'preparing': 1,
          'ready for pickup': 2,
          'completed': 3
        };
        return statusRanks[status.toLowerCase()] || 0;
      };
  
      const statusClass = computed(() => {
        if (!order.value) return {};
        
        const status = order.value.status.toLowerCase();
        return {
          'processing': status === 'order placed',
          'preparing': status === 'preparing',
          'ready': status === 'ready for pickup',
          'completed': status === 'completed'
        };
      });
  
      const estimatedDelivery = computed(() => {
        if (!order.value) return '';
        const date = new Date(order.value.date_created);
        date.setMinutes(date.getMinutes() + 45); // Add 45 minutes for estimated ready time
        return formatTime(date);
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
  
      const fetchOrderDetails = async () => {
        if (!userId || !orderId) {
          error.value = 'Missing user ID or order ID';
          isLoading.value = false;
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5201/get_order_details/${userId}/${orderId}`);
          
          if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
          }
          
          const data = await response.json();
          console.log(data)
          
          if (data.code !== 200) {
            throw new Error(`Server error: ${data.code}`);
          }
          
          order.value = data.data.order;
          isLoading.value = false;
          
          // Initialize map after data is loaded
          initMap();
        } catch (err) {
          console.error('Error fetching order details:', err);
          error.value = err.message || 'Failed to load order details';
          isLoading.value = false;
        }
      };
  
      const confirmPickup = async () => {
        try {
          // In a real app, you would send this update to your backend
          // For now, just update the local state
          order.value.status = 'completed';
          
          // You would typically have an API call like:
          // await fetch(`http://127.0.0.1:5201/update_order_status/${userId}/${orderId}`, {
          //   method: 'POST',
          //   headers: { 'Content-Type': 'application/json' },
          //   body: JSON.stringify({ status: 'completed' })
          // });
          
          alert('Thank you for confirming your order pickup!');
          router.push('/profile');
        } catch (err) {
          console.error('Error confirming pickup:', err);
          error.value = err.message || 'Failed to confirm pickup';
        }
      };
  
      const initMap = () => {
        if (!order.value) return;
        
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
        if (!map.value || !order.value || !order.value.outlet_name.position) return;
        
        // For demo, we'll use a default user location
        // In a real app, you would get this from geolocation API
        const userLocation = { lat: 1.28136, lng: 103.8352 };
        const outletLocation = {
          lat: order.value.outlet_name.position.lat,
          lng: order.value.outlet_name.position.lng
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
          title: order.value.outlet_name.name,
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
            travelMode: google.maps.TravelMode.TRANSIT
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
        fetchOrderDetails();
      });
  
      return {
        orderId,
        isLoading,
        error,
        order,
        statusClass,
        estimatedDelivery,
        formatDate,
        formatTime,
        map,
        directionsPanel,
        confirmPickup
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
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .item-main {
    display: flex;
    justify-content: space-between;
    align-items: center;
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
  
  /* Customization styles */
  .customizations {
    margin-left: 30px;
    margin-top: 0.5rem;
    padding-left: 1rem;
    border-left: 2px solid #f0f0f0;
  }
  
  .customization-item {
    display: flex;
    font-size: 0.85rem;
    color: var(--text-light);
    margin-bottom: 0.25rem;
  }
  
  .customization-name {
    font-weight: 500;
    margin-right: 0.5rem;
  }
  
  .customization-value {
    margin-right: auto;
  }
  
  .customization-price {
    color: var(--primary);
    font-weight: 500;
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
  
  .confirm-pickup {
    margin-top: 1.5rem;
    padding: 1rem;
    background-color: #e6f4ea;
    border-radius: 8px;
    text-align: center;
  }
  
  .confirm-button {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    margin-top: 0.5rem;
    transition: background-color 0.2s;
  }
  
  .confirm-button:hover {
    background-color: var(--primary-dark, #0056b3);
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
  }
  </style>