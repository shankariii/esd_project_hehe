<script setup>
import { ref } from 'vue'


const locations = ref([
    {
        id: 1,
        name: 'Orchard Rd',
        address: '2 Orchard Turn, #B2 - 09, Singapore 238801',
        hours: 'Open Daily: 6am - 8pm'
    },
    {
        id: 2,
        name: 'SMU',
        address: '70 Stamford Rd, #B1-25 Li Ka Shing Library, SMU 178901',
        hours: 'Open Daily: 7am - 7pm'
    },
    {
        id: 3,
        name: 'Changi Airport',
        address: '80 Airport Blvd, Singapore Changi Airport, Singapore 819642',
        hours: 'Open Daily: 6am - 10pm'
    }
]);
</script>

<template>
    <section id="locations" class="section locations">
        <div class="section-heading">
            <h2 style="color: white;">Our Locations</h2>
            <p style="color: rgb(218, 208, 195);">Find us in your neighborhood and experience the Brew Haven difference.
            </p>
        </div>

        <div class="locations-grid">
            <div class="location-card" v-for="location in locations" :key="location.id">
                <div class="location-icon">📍</div>
                <h3 class="location-name">{{ location.name }}</h3>
                <p class="location-address">{{ location.address }}</p>
                <p class="location-hours">{{ location.hours }}</p>
            </div>
        </div>
    </section>
</template>

<style scoped>
.locations {
      background-color: var(--primary);
      color: white;
    }
    
    .locations h2 {
      color: white;
    }
    
    .locations-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .location-card {
      background-color: rgba(255, 255, 255, 0.1);
      padding: 2rem;
      border-radius: 10px;
      text-align: center;
      transition: transform 0.3s;
    }
    
    .location-card:hover {
      transform: translateY(-10px);
    }
    
    .location-icon {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: var(--accent);
    }
    
    .location-name {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    
    .location-address {
      margin-bottom: 1rem;
      opacity: 0.8;
    }
    
    .location-hours {
      font-size: 0.9rem;
      opacity: 0.7;
    }
</style>
