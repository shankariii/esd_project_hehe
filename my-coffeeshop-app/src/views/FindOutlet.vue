<template>
  <div class="outlet-finder-container">
    <!-- Popup Box -->
    <div v-if="isPopupVisible" class="popup-overlay">
      <div class="popup-box">
        <h3>{{ popupTitle }}</h3>
        <p>{{ popupMessage }}</p>
        <button @click="closePopup" class="popup-button">OK</button>
      </div>
    </div>

    <div class="section-heading">
      <h2>Find Your Nearest Outlet</h2>
      <p>Select from our locations or let us find the closest one to you</p>
    </div>
    <div class="finder-layout">
      <!-- Left side: Outlet list and controls -->
      <div class="finder-content">
        <div class="finder-controls">
          <button @click="findNearestOutlet" class="location-btn" :disabled="isLoading">
            <i class="location-icon fa-solid fa-location-dot"></i>
            <span v-if="isLoading">
              <i class="fas fa-spinner fa-spin"></i> Finding...
            </span>
            <span v-else>Find Nearest Outlet</span>
          </button>
          <div class="search-container">
            <input type="text" v-model="searchQuery" placeholder="Search by location name or address"
              class="search-input" @input="filterOutlets" />
            <i class="search-icon fa-solid fa-search"></i>
          </div>
          <div class="sort-controls">
            <label class="sort-label">Sort by:</label>
            <select v-model="sortOption" class="sort-select" @change="sortOutlets">
              <option value="distance">Distance</option>
              <option value="queue">Queue Length</option>
              <option value="name">Name</option>
            </select>
          </div>
        </div>
        <div class="selected-outlet" v-if="selectedOutlet">
          <div class="selected-header">
            <h3>{{ selectedOutlet.name }}</h3>
            <div class="queue-indicator" :class="getQueueClass(selectedOutlet.queueCount)">
              <i class="fa-solid fa-user-group"></i> {{ selectedOutlet.queueCount }} in queue
            </div>
          </div>
          <div class="outlet-details">
            <p><i class="detail-icon fa-solid fa-location-dot"></i> {{ selectedOutlet.address }}</p>
            <p v-if="selectedOutlet.distance"><i class="detail-icon fa-solid fa-route"></i> {{
              formatDistance(selectedOutlet.distance) }}</p>
            <p><i class="detail-icon fa-solid fa-clock"></i> Est. wait: {{
              getEstimatedWaitTime(selectedOutlet.queueCount) }}</p>
          </div>
          <div class="action-buttons">
            <a :href="`https://www.google.com/maps/dir/?api=1&destination=${selectedOutlet.position.lat},${selectedOutlet.position.lng}`"
              target="_blank" class="directions-btn">
              <i class="fa-solid fa-directions"></i> Get Directions
            </a>
            <button class="select-btn" @click="chooseOutlet(selectedOutlet)">
              <i class="fa-solid fa-check"></i> Select This Outlet
            </button>
          </div>
        </div>
        <div class="outlet-list">
          <h3>Available Locations <span class="count-badge">{{ filteredOutlets.length }}</span></h3>
          <div v-if="isOutletsLoading" class="loading-state">
            <i class="fas fa-spinner fa-spin"></i> Loading outlets...
          </div>
          <div v-else-if="filteredOutlets.length === 0" class="no-results">
            <i class="fa-solid fa-face-frown"></i>
            <p>No outlets match your search. Try different keywords.</p>
          </div>
          <div v-else class="list-container">
            <ul class="outlets">
              <li v-for="outlet in filteredOutlets" :key="outlet.id" @click="selectOutlet(outlet)"
                :class="{ active: selectedOutlet && selectedOutlet.id === outlet.id }">
                <div class="outlet-info">
                  <div class="outlet-header">
                    <h4>{{ outlet.name }}</h4>
                    <div class="queue-badge" :class="getQueueClass(outlet.queueCount)">
                      {{ outlet.queueCount }}
                    </div>
                  </div>
                  <p class="outlet-address"><i class="detail-icon fa-solid fa-location-dot"></i> {{ outlet.address }}
                  </p>
                  <div class="outlet-meta">
                    <p v-if="outlet.distance" class="distance-info">
                      <i class="detail-icon fa-solid fa-route"></i> {{ formatDistance(outlet.distance) }}
                    </p>
                    <p class="wait-time">
                      <i class="detail-icon fa-solid fa-clock"></i>
                      {{ getEstimatedWaitTime(outlet.queueCount) }}
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <!-- Right side: Map -->
      <div class="map-wrapper">
        <div id="map" ref="mapRef" class="map-container"></div>
        <!-- Map legend -->
        <div class="map-legend">
          <h4>Queue Status</h4>
          <div class="legend-item">
            <span class="legend-dot queue-empty"></span>
            <span>No Queue</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot queue-low"></span>
            <span>Short Wait (1-4)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot queue-medium"></span>
            <span>Medium Wait (5-9)</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot queue-high"></span>
            <span>Long Wait (10+)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'OutletFinder',
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      map: null,
      markers: [],
      infoWindow: null,
      userLocation: null,
      selectedOutlet: null,
      isLoading: false,
      isOutletsLoading: true,
      outlets: [],
      filteredOutlets: [],
      searchQuery: '',
      sortOption: 'distance',
      userMarker: null,
      // Popup state
      isPopupVisible: false,
      popupTitle: '',
      popupMessage: '',
    };
  },
  computed: {
    sortedOutlets() {
      return this.filteredOutlets;
    }
  },
  mounted() {
    this.loadGoogleMapsScript();
    this.fetchOutlets();
    this.addFontAwesome();
    // Check if there was a previously selected outlet
    const savedOutletId = localStorage.getItem("selectedOutletId");
    if (savedOutletId) {
      // Mark it as something to select once outlets are loaded
      this.savedOutletId = savedOutletId;
    }
  },
  methods: {
    showPopup(title, message) {
      this.popupTitle = title;
      this.popupMessage = message;
      this.isPopupVisible = true;
    },
    closePopup() {
      this.isPopupVisible = false;
    },
    addFontAwesome() {
      const link = document.createElement('link');
      link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
      link.rel = 'stylesheet';
      document.head.appendChild(link);
    },
    async fetchOutlets() {
      try {
        const response = await axios.get('http://localhost:5001/outlets');
        // First get all outlets
        this.outlets = response.data.map(outlet => ({
          ...outlet,
          position: outlet.position || { lat: 0, lng: 0 },
          queueCount: outlet.queueCount || 0 // Temporary default
        }));
        // Then fetch queue counts for each outlet
        await Promise.all(this.outlets.map(async (outlet) => {
          try {
            const countResponse = await axios.get(`http://127.0.0.1:5500/orders/count?outlet_id=${outlet.id}`);
            outlet.queueCount = countResponse.data.total_orders || 0;
          } catch (error) {
            console.error(`Failed to fetch queue count for outlet ${outlet.id}:`, error);
            outlet.queueCount = 0; // Default to 0 if there's an error
          }
        }));
        this.filteredOutlets = [...this.outlets];
        // If there was a previously selected outlet, select it
        if (this.savedOutletId) {
          const savedOutlet = this.outlets.find(o => o.id === this.savedOutletId);
          if (savedOutlet) {
            this.selectOutlet(savedOutlet);
          }
        }
        // Check if map is already initialized
        if (this.map) {
          this.addMarkers();
        }
      } catch (error) {
        console.error('Failed to fetch outlets:', error);
        this.showPopup('Error', 'Unable to load outlets. Please try again later.');
      } finally {
        this.isOutletsLoading = false;
      }
    },
    chooseOutlet(outlet) {
      this.showPopup('Success', `${outlet.name} has been selected`);
      localStorage.setItem("selectedOutletId", outlet.id);
      localStorage.setItem("selectedOutletName", outlet.name);
      setTimeout(() => {
        this.$router.push('/');
      });
    },
    loadGoogleMapsScript() {
      if (window.google && window.google.maps) {
        this.initMap();
        return;
      }
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDyzGN00mpIu7qElBpIFwiPjWyQlkIfHHM&callback=initMap`;
      script.defer = true;
      window.initMap = this.initMap;
      document.head.appendChild(script);
    },
    initMap() {
      const singaporeCenter = { lat: 1.3521, lng: 103.8198 };
      this.map = new google.maps.Map(this.$refs.mapRef, {
        center: singaporeCenter,
        zoom: 12,
        styles: [
          { featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] }
        ],
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: true,
        zoomControlOptions: {
          position: google.maps.ControlPosition.RIGHT_CENTER
        }
      });
      this.infoWindow = new google.maps.InfoWindow();
      // If outlets are already loaded, add markers now
      if (this.outlets.length > 0) {
        this.addMarkers();
      }
      // Auto find nearest outlet if geolocation permission is already granted
      navigator.permissions?.query({ name: 'geolocation' })
        .then((result) => {
          if (result.state === 'granted') {
            this.findNearestOutlet();
          }
        });
    },
    addMarkers() {
      this.markers.forEach(marker => marker.setMap(null));
      this.markers = [];
      // Fit bounds to all markers
      const bounds = new google.maps.LatLngBounds();
      this.outlets.forEach(outlet => {
        // Skip if position is invalid
        if (!outlet.position || (!outlet.position.lat && !outlet.position.lng)) {
          console.error('Invalid position for outlet:', outlet);
          return;
        }
        const marker = new google.maps.Marker({
          position: outlet.position,
          map: this.map,
          title: outlet.name,
          animation: google.maps.Animation.DROP,
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: this.getMarkerColor(outlet.queueCount),
            fillOpacity: 1,
            strokeColor: '#FFFFFF',
            strokeWeight: 2,
            scale: 10
          }
        });
        marker.addListener('click', () => this.selectOutlet(outlet));
        this.markers.push(marker);
        bounds.extend(outlet.position);
      });
      // If we have markers, fit map to show all of them
      if (this.markers.length > 0) {
        this.map.fitBounds(bounds);
        // Don't zoom in too far
        const listener = google.maps.event.addListener(this.map, "idle", () => {
          if (this.map.getZoom() > 15) this.map.setZoom(15);
          google.maps.event.removeListener(listener);
        });
      }
    },
    findNearestOutlet() {
      this.isLoading = true;
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          position => {
            this.userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            // Remove previous user marker if exists
            if (this.userMarker) {
              this.userMarker.setMap(null);
            }
            this.userMarker = new google.maps.Marker({
              position: this.userLocation,
              map: this.map,
              title: "Your Location",
              icon: {
                url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                scaledSize: new google.maps.Size(40, 40)
              },
              zIndex: 1000, // Ensure it's on top
              animation: google.maps.Animation.DROP
            });
            this.map.setCenter(this.userLocation);
            this.map.setZoom(13);
            this.calculateDistances();
          },
          error => {
            console.error("Error getting location:", error);
            this.showPopup('Error', "Unable to get your location. Please select an outlet manually.");
            this.isLoading = false;
          },
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          }
        );
      } else {
        this.showPopup('Error', "Geolocation is not supported by your browser");
        this.isLoading = false;
      }
    },
    calculateDistances() {
      if (!this.userLocation) return;
      const service = new google.maps.DistanceMatrixService();
      const destinations = this.outlets.map(outlet => outlet.position);
      service.getDistanceMatrix(
        {
          origins: [this.userLocation],
          destinations,
          travelMode: google.maps.TravelMode.DRIVING,
          unitSystem: google.maps.UnitSystem.METRIC
        },
        (response, status) => {
          if (status === "OK" && response.rows[0].elements) {
            const results = response.rows[0].elements;
            this.outlets.forEach((outlet, index) => {
              if (results[index] && results[index].status === "OK") {
                outlet.distance = results[index].distance.value;
                outlet.duration = results[index].duration.text;
              }
            });
            // Update filtered outlets
            this.filterOutlets();
            // Sort outlets by distance
            this.sortOption = 'distance';
            this.sortOutlets();
            // Select nearest outlet with reasonable queue
            let nearestOutlets = [...this.outlets]
              .filter(o => o.distance !== undefined)
              .sort((a, b) => a.distance - b.distance);
            // Try to find a nearby outlet with a short queue first
            let bestOutlet = nearestOutlets.find(o =>
              o.distance < 5000 && o.queueCount < 5);
            // If not found, just use the closest one
            if (!bestOutlet && nearestOutlets.length > 0) {
              bestOutlet = nearestOutlets[0];
            }
            if (bestOutlet) {
              this.selectOutlet(bestOutlet);
              this.showPopup('Success', `Found nearest outlet: ${bestOutlet.name}`);
            }
            this.isLoading = false;
          } else {
            console.error("Distance Matrix request failed due to", status);
            this.isLoading = false;
            this.showPopup('Error', "Unable to calculate distances. Please select an outlet manually.");
          }
        }
      );
    },
    selectOutlet(outlet) {
      this.selectedOutlet = outlet;
      if (this.map && outlet.position) {
        this.map.setCenter(outlet.position);
        this.map.setZoom(15);
        // Highlight the selected marker
        const markerIndex = this.outlets.findIndex(o => o.id === outlet.id);
        if (markerIndex >= 0 && this.markers[markerIndex]) {
          // Bounce animation for the selected marker
          this.markers[markerIndex].setAnimation(google.maps.Animation.BOUNCE);
          // Stop the animation after 1.5 seconds
          setTimeout(() => {
            this.markers[markerIndex].setAnimation(null);
          }, 1500);
        }
        this.infoWindow.setContent(`
          <div class="info-window">
            <h3>${outlet.name}</h3>
            <p>${outlet.address}</p>
            ${outlet.distance ? `<p><strong>Distance:</strong> ${this.formatDistance(outlet.distance)}</p>` : ''}
            <p><strong>Queue:</strong> <span style="color: ${this.getMarkerColor(outlet.queueCount)}; font-weight: bold;">${outlet.queueCount} people waiting</span></p>
            <p><strong>Estimated wait:</strong> ${this.getEstimatedWaitTime(outlet.queueCount)}</p>
          </div>
        `);
        const markerToUse = this.markers[this.outlets.indexOf(outlet)];
        if (markerToUse) {
          this.infoWindow.open(this.map, markerToUse);
        }
      }
      // Scroll the selected outlet into view in the list
      this.$nextTick(() => {
        const activeElement = document.querySelector('.outlets li.active');
        if (activeElement) {
          activeElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      });
    },
    formatDistance(meters) {
      if (meters === undefined || meters === null) return "";
      return meters < 1000 ? `${meters} m` : `${(meters / 1000).toFixed(1)} km`;
    },
    getQueueClass(count) {
      if (count === 0) return 'queue-empty';
      if (count < 5) return 'queue-low';
      if (count < 10) return 'queue-medium';
      return 'queue-high';
    },
    getMarkerColor(count) {
      if (count === 0) return '#4CAF50';
      if (count < 5) return '#8BC34A';
      if (count < 10) return '#FFC107';
      return '#F44336';
    },
    getEstimatedWaitTime(count) {
      if (count === 0) return 'No wait';
      const minutes = count * 3;
      return minutes < 60 ? `${minutes} min` : `${Math.floor(minutes / 60)}h ${minutes % 60}m`;
    },
    filterOutlets() {
      if (!this.searchQuery.trim()) {
        this.filteredOutlets = [...this.outlets];
      } else {
        const query = this.searchQuery.toLowerCase().trim();
        this.filteredOutlets = this.outlets.filter(outlet => {
          return outlet.name.toLowerCase().includes(query) ||
            outlet.address.toLowerCase().includes(query);
        });
      }
      this.sortOutlets();
    },
    sortOutlets() {
      switch (this.sortOption) {
        case 'distance':
          // Sort by distance if available, otherwise put them at the end
          this.filteredOutlets.sort((a, b) => {
            if (a.distance === undefined && b.distance === undefined) return 0;
            if (a.distance === undefined) return 1;
            if (b.distance === undefined) return -1;
            return a.distance - b.distance;
          });
          break;
        case 'queue':
          this.filteredOutlets.sort((a, b) => a.queueCount - b.queueCount);
          break;
        case 'name':
          this.filteredOutlets.sort((a, b) => a.name.localeCompare(b.name));
          break;
      }
    },
  }
};
</script>

<style scoped>
.outlet-finder-container {
  max-width: 1200px;
  margin: 6rem auto;
  padding: 2rem 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.section-heading {
  text-align: center;
  margin-bottom: 2rem;
}

.section-heading h2 {
  font-size: 2rem;
  color: var(--primary, #333);
  margin-bottom: 0.5rem;
}

.section-heading p {
  color: var(--text-light, #666);
  font-size: 1.1rem;
}

.finder-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.finder-controls {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.location-btn {
  background-color: var(--primary, #4361ee);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 4px 6px rgba(67, 97, 238, 0.2);
  font-size: 1rem;
}

.location-btn:hover {
  background-color: var(--dark, #3a56d4);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(67, 97, 238, 0.3);
}

.location-btn:active {
  transform: translateY(0);
}

.location-btn:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.location-icon,
.detail-icon {
  font-size: 1rem;
}

.search-container {
  position: relative;
  margin-top: 0.5rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: var(--primary, #4361ee);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
  outline: none;
}

.search-icon {
  position: absolute;
  left: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  color: #777;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 0.5rem;
}

.sort-label {
  font-weight: 500;
  color: #555;
}

.sort-select {
  flex-grow: 1;
  padding: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: white;
  font-size: 0.9rem;
}

.map-wrapper {
  position: relative;
}

.map-container {
  height: 100%;
  min-height: 600px;
  width: 100%;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  /* top: 100px; */
  border: 1px solid #eaeaea;
}

.map-legend {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background-color: white;
  padding: 10px 15px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1;
  max-width: 200px;
  border: 1px solid #eaeaea;
}

.map-legend h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 5px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
  font-size: 0.8rem;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
  display: inline-block;
}

.outlet-list {
  margin-top: 1rem;
}

.outlet-list h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: var(--primary, #333);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.count-badge {
  background-color: var(--primary, #4361ee);
  color: white;
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 20px;
  display: inline-block;
}

.list-container {
  max-height: 600px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #ddd #f5f5f5;
  border-radius: 10px;
  padding-right: 5px;
}

.list-container::-webkit-scrollbar {
  width: 8px;
}

.list-container::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 10px;
}

.list-container::-webkit-scrollbar-thumb {
  background-color: #ddd;
  border-radius: 10px;
}

.outlets {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 0;
  padding: 0;
}

.outlets li {
  background-color: white;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
  position: relative;
}

.outlets li:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.outlets li.active {
  border-left: 4px solid var(--accent);
  background-color: rgba(255, 152, 0, 0.03);
}

.outlet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.outlet-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 0.75rem;
  font-size: 0.9rem;
  gap: 1rem;
}

.outlets h4 {
  color: var(--dark, #333);
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.outlet-address {
  color: var(--text-light, #666);
  margin: 0.5rem 0;
  font-size: 0.95rem;
  line-height: 1.4;
}

.distance-info,
.wait-time {
  color: var(--text-light, #666);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.queue-badge {
  display: inline-flex;
  min-width: 28px;
  height: 28px;
  border-radius: 14px;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 0.85rem;
  padding: 0 8px;
}

.selected-outlet {
  background-color: white;
  padding: 1.5rem;
  border-radius: 10px;
  border-left: 4px solid var(--accent, #ff9800);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  animation: highlight 1s ease;
}

@keyframes highlight {
  0% {
    background-color: rgba(255, 152, 0, 0.2);
  }

  100% {
    background-color: white;
  }
}

.selected-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.selected-outlet h3 {
  color: var(--primary, #333);
  margin: 0;
  font-size: 1.4rem;
}

.queue-indicator {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.outlet-details {
  margin-bottom: 1.25rem;
}

.outlet-details p {
  margin: 0.75rem 0;
  color: var(--text-light, #666);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.directions-btn,
.select-btn {
  padding: 0.75rem 1.2rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
  cursor: pointer;
}

.directions-btn {
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.directions-btn:hover {
  background-color: #eaeaea;
  border-color: #ccc;
}

.select-btn {
  background-color: var(--accent, #ff9800);
  color: white;
  border: none;
  box-shadow: 0 4px 10px rgba(255, 152, 0, 0.2);
}

.select-btn:hover {
  background-color: var(--accent-dark, #f57c00);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(255, 152, 0, 0.3);
}

.select-btn:active {
  transform: translateY(0);
}

/* Queue status colors */
.queue-empty {
  background-color: #4CAF50;
  color: white;
}

.queue-low {
  background-color: #8BC34A;
  color: white;
}

.queue-medium {
  background-color: #FFC107;
  color: #333;
}

.queue-high {
  background-color: #F44336;
  color: white;
}

/* Loading and error states */
.loading-state,
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: #777;
  background-color: #f9f9f9;
  border-radius: 8px;
  text-align: center;
}

.loading-state i,
.no-results i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #aaa;
}

/* Info window styling */
.info-window {
  padding: 0.5rem;
  max-width: 250px;
}

.info-window h3 {
  font-size: 1.1rem;
  margin: 0 0 5px 0;
  color: var(--primary, #333);
}

.info-window p {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #555;
}

/* Responsive styles */
@media (max-width: 992px) {
  .finder-layout {
    grid-template-columns: 1fr;
  }

  .map-container {
    min-height: 400px;
    position: relative;
    top: 0;
  }

  .action-buttons {
    flex-direction: column;
  }

  .directions-btn,
  .select-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .outlet-finder-container {
    padding: 1rem 0.5rem;
  }

  .selected-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .queue-indicator {
    align-self: flex-start;
  }

  .sort-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .sort-select {
    width: 100%;
  }
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
</style>