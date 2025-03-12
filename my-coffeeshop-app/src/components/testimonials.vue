<script setup>
import { ref } from 'vue'


const testimonials = ref([
    {
        id: 1,
        text: "I've tried coffee shops all over the city, and Brew Haven consistently delivers the best latte I've ever had. The atmosphere is perfect for both quick stops and longer work sessions.",
        author: 'Michael T.',
        title: 'Local Resident'
    },
    {
        id: 2,
        text: 'As someone who works remotely, I spend a lot of time in cafes. Brew Haven has become my second office - great wifi, friendly staff, and their cold brew keeps me going all day!',
        author: 'Samantha K.',
        title: 'Freelance Designer'
    }
]);
</script>

<template>
    <section class="section testimonials">
        <div class="section-heading">
            <h2>What Our Customers Say</h2>
            <p>The voices that keep us brewing better every day.</p>
        </div>

        <div class="testimonials-container">
            <div class="testimonial" v-for="testimonial in testimonials" :key="testimonial.id">
                <p class="testimonial-text">{{ testimonial.text }}</p>
                <div class="testimonial-author">
                    <img :src="`/api/placeholder/100/100?text=${encodeURIComponent(testimonial.author)}`"
                        :alt="testimonial.author" class="author-img">
                    <div class="author-info">
                        <h4>{{ testimonial.author }}</h4>
                        <p>{{ testimonial.title }}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.testimonials {
      background-color: var(--light);
    }
    
    .testimonials-container {
      max-width: 800px;
      margin: 0 auto;
    }
    
    .testimonial {
      background-color: white;
      padding: 2rem;
      border-radius: 10px;
      margin-bottom: 2rem;
      box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .testimonial-text {
      font-style: italic;
      margin-bottom: 1.5rem;
      color: var(--text);
      font-size: 1.1rem;
    }
    
    .testimonial-author {
      display: flex;
      align-items: center;
    }
    
    .author-img {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      margin-right: 1rem;
      object-fit: cover;
    }
    
    .author-info h4 {
      font-size: 1.1rem;
      margin-bottom: 0.2rem;
    }
    
    .author-info p {
      font-size: 0.9rem;
      color: var(--text-light);
    }
</style>
