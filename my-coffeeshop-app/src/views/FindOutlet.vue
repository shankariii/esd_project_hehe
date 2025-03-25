<template>
    <div class="outlet-finder-container">
      <div class="section-heading">
        <h2>Find Your Nearest Outlet</h2>
        <p>Select from our locations or let us find the closest one to you</p>
      </div>
      
      <div class="finder-layout">
        <!-- Left side: Outlet list and controls -->
        <div class="finder-content">
          <div class="finder-controls">
            <button 
              @click="findNearestOutlet" 
              class="location-btn"
              :disabled="isLoading"
            >
              <i class="location-icon">📍</i>
              <span v-if="isLoading">Finding...</span>
              <span v-else>Find Nearest Outlet</span>
            </button>
            
            <div class="selected-outlet" v-if="selectedOutlet">
              <div class="selected-header">
                <!-- <h3>{{ selectedOutlet.name }}</h3> -->
                <h3><a :href="`https://www.google.com/maps/dir/?api=1&destination=${selectedOutlet.position.lat},${selectedOutlet.position.lng}`" 
                 target="_blank">
                {{selectedOutlet.name}}
              </a></h3>
                <div class="queue-indicator" :class="getQueueClass(selectedOutlet.queueCount)">
                  {{ selectedOutlet.queueCount }} in queue
                </div>
              </div>
              <div class="outlet-details">
                <p><i class="detail-icon"></i> {{ selectedOutlet.address }}</p>
                <p v-if="selectedOutlet.distance"><i class="detail-icon"></i> {{ formatDistance(selectedOutlet.distance) }}</p>
              </div>
              <a class="directions-btn" @click="chooseOutlet(selectedOutlet.id)">
                Select
              </a>
            </div>
          </div>
          
          <div class="outlet-list">
            <h3>All Locations</h3>
            <ul class="outlets">
              <li 
                v-for="outlet in sortedOutlets" 
                :key="outlet.id"
                @click="selectOutlet(outlet)"
                :class="{ active: selectedOutlet && selectedOutlet.id === outlet.id }"
              >
                <div class="outlet-info">
                  <div class="outlet-header">
                    <h4>{{ outlet.name }}</h4>
                    <div class="queue-badge" :class="getQueueClass(outlet.queueCount)">
                      {{ outlet.queueCount }}
                    </div>
                  </div>
                  <p class="outlet-address"><i class="detail-icon"></i> {{ outlet.address }}</p>
                  <div class="outlet-meta">
                    <p v-if="outlet.distance" class="distance-info">
                      <i class="detail-icon"></i> {{ formatDistance(outlet.distance) }}
                    </p>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        
        <!-- Right side: Map -->
        <div id="map" ref="mapRef" class="map-container"></div>
      </div>
    </div>
  </template>
  
  <script>
   import { useRouter } from 'vue-router';
  export default {
    name: 'OutletFinder',
    setuo(){
      const router = useRouter();
    },
    data() {
      return {
        map: null,
        markers: [],
        infoWindow: null,
        userLocation: null,
        selectedOutlet: null,
        isLoading: false,
        outlets: [
          {
            id: 1,
            name: "Orchard Road Branch",
            position: { lat: 1.3024, lng: 103.8324 },
            address: "313 Orchard Road, #01-25, Singapore 238895",
            queueCount: 12
          },
          {
            id: 2,
            name: "Jurong East Mall",
            position: { lat: 1.3329, lng: 103.7436 },
            address: "50 Jurong Gateway Road, #02-15, Singapore 608549",
            queueCount: 5
          },
          {
            id: 3,
            name: "Marina Bay Sands",
            position: { lat: 1.2836, lng: 103.8605 },
            address: "10 Bayfront Avenue, #B2-54, Singapore 018956",
            queueCount: 0
          },
          {
            id: 4,
            name: "Tampines Mall",
            position: { lat: 1.3522, lng: 103.9448 },
            address: "4 Tampines Central 5, #03-22, Singapore 529510",
            queueCount: 3
          },
          {
            id: 5,
            name: "VivoCity",
            position: { lat: 1.2644, lng: 103.8222 },
            address: "1 HarbourFront Walk, #02-10, Singapore 098585",
            queueCount: 8
          }
        ]
      }
    },
    computed: {
      sortedOutlets() {
        // If we have user location and distances, sort by distance
        if (this.userLocation && this.outlets.some(o => o.distance)) {
          return [...this.outlets].sort((a, b) => {
            // Default to Infinity if distance is not calculated yet
            const distA = a.distance || Infinity;
            const distB = b.distance || Infinity;
            return distA - distB;
          });
        }
        // Otherwise sort by queue length (shortest first)
        return [...this.outlets].sort((a, b) => a.queueCount - b.queueCount);
      }
    },
    mounted() {
      this.loadGoogleMapsScript();
    },
    methods: {
      chooseOutlet(outletId){
        console.log("hello")
        alert("Outlet has been selected")
        localStorage.setItem("selectedOutletId",outletId )
        // const router = useRouter();
        this.router.push(`/drinksy`)
      },
      loadGoogleMapsScript() {
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDyzGN00mpIu7qElBpIFwiPjWyQlkIfHHM&callback=initMap`;
        script.async = true;
        script.defer = true;
        window.initMap = this.initMap;
        document.head.appendChild(script);
      },
      initMap() {
        // Center map on Singapore as default
        const singaporeCenter = { lat: 1.3521, lng: 103.8198 };
        
        this.map = new google.maps.Map(this.$refs.mapRef, {
          center: singaporeCenter,
          zoom: 12,
          // No custom styles - using default Google Maps style
        });
        
        this.infoWindow = new google.maps.InfoWindow();
        
        // Add markers for all outlets
        this.outlets.forEach(outlet => {
          const marker = new google.maps.Marker({
            position: outlet.position,
            map: this.map,
            title: outlet.name,
            // Using standard marker with custom color based on queue
            icon: {
              path: google.maps.SymbolPath.CIRCLE,
              fillColor: this.getMarkerColor(outlet.queueCount),
              fillOpacity: 1,
              strokeColor: '#FFFFFF',
              strokeWeight: 2,
              scale: 8
            }
          });
          
          marker.addListener('click', () => {
            this.selectOutlet(outlet);
          });
          
          this.markers.push(marker);
        });
      },
      findNearestOutlet() {
        this.isLoading = true;
        
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              this.userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };
              
              // Add user marker
              const userMarker = new google.maps.Marker({
                position: this.userLocation,
                map: this.map,
                title: "Your Location",
                icon: {
                  url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                }
              });
              
              // Center map on user location
              this.map.setCenter(this.userLocation);
              this.map.setZoom(13);
              
              // Calculate distances and find nearest
              this.calculateDistances();
              this.isLoading = false;
            },
            (error) => {
              console.error("Error getting location:", error);
              alert("Unable to get your location. Please select an outlet from the list.");
              this.isLoading = false;
            }
          );
        } else {
          alert("Geolocation is not supported by your browser");
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
            destinations: destinations,
            travelMode: google.maps.TravelMode.DRIVING
          },
          (response, status) => {
            if (status === "OK") {
              const results = response.rows[0].elements;
              
              // Update outlets with distance information
              this.outlets.forEach((outlet, index) => {
                if (results[index].status === "OK") {
                  outlet.distance = results[index].distance.value; // in meters
                  outlet.duration = results[index].duration.text;
                }
              });
              
              // Find and select nearest outlet
              const nearestOutlet = [...this.outlets].sort((a, b) => a.distance - b.distance)[0];
              this.selectOutlet(nearestOutlet);
            } else {
              console.error("Distance Matrix request failed due to", status);
            }
          }
        );
      },
      selectOutlet(outlet) {
        this.selectedOutlet = outlet;
        
        // Center map on selected outlet
        this.map.setCenter(outlet.position);
        this.map.setZoom(15);
        
        // Show info window
        this.infoWindow.setContent(`
          <div class="info-window">
            <h3>${outlet.name}</h3>
            <p>${outlet.address}</p>
            ${outlet.distance ? `<p><strong>Distance:</strong> ${this.formatDistance(outlet.distance)}</p>` : ''}
            <p><strong>Queue:</strong> <span style="color: ${this.getMarkerColor(outlet.queueCount)}; font-weight: bold;">${outlet.queueCount} people waiting</span></p>
            <p><strong>Estimated wait:</strong> ${this.getEstimatedWaitTime(outlet.queueCount)}</p>
          </div>
        `);
        
        this.infoWindow.open(this.map, this.markers[this.outlets.indexOf(outlet)]);
      },
      formatDistance(meters) {
        if (meters < 1000) {
          return `${meters} m`;
        } else {
          return `${(meters / 1000).toFixed(1)} km`;
        }
      },
      getQueueClass(count) {
        if (count === 0) return 'queue-empty';
        if (count < 5) return 'queue-low';
        if (count < 10) return 'queue-medium';
        return 'queue-high';
      },
      getMarkerColor(count) {
        if (count === 0) return '#4CAF50'; // Green for no queue
        if (count < 5) return '#8BC34A'; // Light green for short queue
        if (count < 10) return '#FFC107'; // Amber for medium queue
        return '#F44336'; // Red for long queue
      },
      getEstimatedWaitTime(count) {
        // Assume average of 3 minutes per person
        if (count === 0) return 'No wait';
        const minutes = count * 3;
        if (minutes < 60) {
          return `${minutes} min`;
        } else {
          const hours = Math.floor(minutes / 60);
          const remainingMinutes = minutes % 60;
          return `${hours}h ${remainingMinutes}m`;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .outlet-finder-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
  
  .finder-layout {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 2rem;
  }
  
  .finder-controls {
    margin-bottom: 2rem;
  }
  
  .location-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 5px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .location-btn:hover {
    background-color: var(--dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  .location-btn:active {
    transform: translateY(0);
  }
  
  .location-btn:disabled {
    background-color: var(--text-light);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  .location-icon, .detail-icon {
    display: inline-block;
    margin-right: 5px;
  }
  
  .map-container {
    height: 90%;
    min-height: 500px;
    width: 100%;
    border-radius: 10px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
    position: sticky;
    top: 100px;
  }
  
  .outlet-list {
    margin-top: 2rem;
  }
  
  .outlet-list h3 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: var(--primary);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.5rem;
    display: inline-block;
  }
  
  .outlets {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
    padding: 0;
  }
  
  .outlets li {
    background-color: white;
    border-radius: 10px;
    padding: 1.25rem;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    border-left: 4px solid transparent;
  }
  
  .outlets li:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.12);
  }
  
  .outlets li.active {
    border-left: 4px solid var(--accent);
    background-color: rgba(255, 202, 40, 0.05);
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
    margin-top: 0.5rem;
    font-size: 0.9rem;
  }
  
  .outlets h4 {
    color: var(--dark);
    margin: 0;
    font-size: 1.1rem;
  }
  
  .outlet-address {
    color: var(--text-light);
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
  }
  
  .distance-info, .queue-text {
    color: var(--text-light);
    margin: 0;
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
    font-size: 0.8rem;
    padding: 0 8px;
  }
  
  .selected-outlet {
    background-color: white;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid var(--accent);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    margin-top: 1.5rem;
  }
  
  .selected-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }
  
  .selected-outlet h3 {
    color: var(--primary);
    margin: 0;
    font-size: 1.3rem;
  }
  
  .queue-indicator {
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .outlet-details {
    margin-bottom: 1.25rem;
  }
  
  .outlet-details p {
    margin-bottom: 0.5rem;
    color: var(--text-light);
  }
  
  .directions-btn {
    display: inline-block;
    background-color: var(--secondary);
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 500;
    transition: background-color 0.3s;
    margin-top: 0.5rem;
  }
  
  .directions-btn:hover {
    background-color: var(--dark);
  }
  
  .queue-empty {
    color: white;
    background-color: #4CAF50;
  }
  
  .queue-low {
    color: white;
    background-color: #8BC34A;
  }
  
  .queue-medium {
    color: #333;
    background-color: #FFC107;
  }
  
  .queue-high {
    color: white;
    background-color: #F44336;
  }
  
  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .finder-layout {
      grid-template-columns: 1fr;
    }
    
    .map-container {
      min-height: 100px;
      position: relative;
      top: 0;
      margin-bottom: 1.5rem;
      order: -1;
    }
    
    .finder-content {
      order: 2;
    }
    
    .selected-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
    
    .queue-indicator {
      align-self: flex-start;
    }
    
    .outlet-meta {
      flex-direction: column;
      gap: 0.25rem;
    }
  }
  
  /* Small screen adjustments */
  @media (max-width: 480px) {
    .outlet-header {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .queue-badge {
      margin-top: 0.5rem;
    }
    
    .outlets li {
      padding: 1rem;
    }
    
    .selected-outlet {
      padding: 1.25rem;
    }
  }
  </style>