<template>
    <div class="menu-container">
        <header class="menu-header">
            <div class="container">
                <h1>Our Menu</h1>
                <p>Discover our handcrafted beverages, made with love</p>
            </div>
        </header>

        <div class="menu-controls container">
            <div class="search-box">
                <input type="text" v-model="searchQuery" placeholder="Search drinks..." @input="filterDrinks">
                <button class="search-icon">
                    <i class="fa fa-search"></i>
                </button>
            </div>

            <!-- <div class="filter-controls">
          <div class="filter-group">
            <label>Category</label>
            <select v-model="selectedCategory" @change="filterDrinks">
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
  
          <div class="filter-group">
            <label>Price Range</label>
            <div class="price-slider">
              <input 
                type="range" 
                v-model="priceRange" 
                :min="minPrice" 
                :max="maxPrice" 
                step="0.5" 
                @input="filterDrinks"
              >
              <span>${{ priceRange }}</span>
            </div>
          </div>
  
          <button class="reset-btn" @click="resetFilters">Reset Filters</button>
        </div> -->
        </div>

        <div class="menu-content container">
            <div v-if="filteredDrinks.length === 0" class="no-results">
                <p>No drinks match your search criteria. Try adjusting your filters.</p>
            </div>

            <div v-else class="drinks-grid">
                <div v-for="drink in filteredDrinks" :key="drink.id" class="drink-card" @click="goToDrinkCustomization(drink.id)">
                    <div class="drink-image">
                        <img :src="drink.image" :alt="drink.name">
                        <!-- <span v-if="drink.featured" class="featured-badge">Featured</span> -->
                    </div>

                    <div class="drink-info">
                        <h3>{{ drink.name }}</h3>
                        <p class="drink-description">{{ drink.description }}</p>
                        <div class="drink-meta">
                            <!-- <span class="drink-category">{{ drink.category }}</span> -->
                            <span class="drink-price">${{ drink.price.toFixed(2) }}</span>
                            <button class="add-to-cart-btn" @click="goToDrinkCustomization(drink.id)">Add to
                                Cart</button>
                        </div>

                    </div>
                </div>
            </div>
        </div>

        <div class="pagination container">
            <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)" class="page-btn">
                Previous
            </button>

            <span class="page-info">{{ currentPage }} of {{ totalPages }}</span>

            <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)" class="page-btn">
                Next
            </button>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';

export default {
    name: 'MenuComponent',
    setup() {
        // State variables
        const searchQuery = ref('')
        const selectedCategory = ref('')
        const priceRange = ref(15)
        const currentPage = ref(1)
        const itemsPerPage = ref(8)

        // Sample drink data (this would come from Firebase in a real app)
        const allDrinks = ref([
            {
                id: 1,
                name: 'Classic Espresso',
                description: 'Strong and bold single shot of pure coffee essence',
                category: 'Espresso',
                price: 3.50,
                image: '/images/espresso.jpg',
                featured: true
            },
            {
                id: 2,
                name: 'Cappuccino',
                description: 'Perfect balance of espresso, steamed milk, and foam',
                category: 'Milk-based',
                price: 4.75,
                image: '/images/cappuccino.jpg',
                featured: false
            },
            {
                id: 3,
                name: 'Caramel Macchiato',
                description: 'Espresso with vanilla syrup, milk and caramel drizzle',
                category: 'Specialty',
                price: 5.50,
                image: '/images/caramel-macchiato.jpg',
                featured: true
            },
            {
                id: 4,
                name: 'Cold Brew',
                description: 'Smooth, low-acidity coffee brewed with cold water for 24 hours',
                category: 'Iced',
                price: 4.95,
                image: '/images/cold-brew.jpg',
                featured: false
            },
            {
                id: 5,
                name: 'Mocha Frappuccino',
                description: 'Blended coffee with chocolate, milk and ice, topped with whipped cream',
                category: 'Blended',
                price: 6.25,
                image: '/images/mocha-frappuccino.jpg',
                featured: false
            },
            {
                id: 6,
                name: 'Americano',
                description: 'Espresso diluted with hot water for a lighter flavor profile',
                category: 'Espresso',
                price: 3.75,
                image: '/images/americano.jpg',
                featured: false
            },
            {
                id: 7,
                name: 'Chai Tea Latte',
                description: 'Spiced black tea with steamed milk and honey',
                category: 'Tea',
                price: 4.50,
                image: '/images/chai-latte.jpg',
                featured: false
            },
            {
                id: 8,
                name: 'Nitro Cold Brew',
                description: 'Cold brew infused with nitrogen for a creamy, cascading texture',
                category: 'Iced',
                price: 5.75,
                image: '/images/nitro-cold-brew.jpg',
                featured: true
            },
            {
                id: 9,
                name: 'Flat White',
                description: 'Ristretto shots with steamed milk and minimal foam',
                category: 'Milk-based',
                price: 4.95,
                image: '/images/flat-white.jpg',
                featured: false
            },
            {
                id: 10,
                name: 'Pumpkin Spice Latte',
                description: 'Espresso with pumpkin spice syrup, steamed milk and whipped cream',
                category: 'Seasonal',
                price: 5.95,
                image: '/images/pumpkin-spice.jpg',
                featured: true
            },
            {
                id: 11,
                name: 'Matcha Green Tea Latte',
                description: 'Stone-ground matcha powder with steamed milk',
                category: 'Tea',
                price: 5.25,
                image: '/images/matcha-latte.jpg',
                featured: false
            },
            {
                id: 12,
                name: 'Affogato',
                description: 'Vanilla ice cream "drowned" with a shot of hot espresso',
                category: 'Specialty',
                price: 6.50,
                image: '/images/affogato.jpg',
                featured: false
            }
        ])

        // Computed properties
        const filteredDrinks = ref([])

        const categories = computed(() => {
            const uniqueCategories = new Set(allDrinks.value.map(drink => drink.category))
            return [...uniqueCategories]
        })

        const minPrice = computed(() => {
            return Math.floor(Math.min(...allDrinks.value.map(drink => drink.price)))
        })

        const maxPrice = computed(() => {
            return Math.ceil(Math.max(...allDrinks.value.map(drink => drink.price)))
        })

        const totalPages = computed(() => {
            return Math.ceil(filteredDrinks.value.length / itemsPerPage.value)
        })

        const paginatedDrinks = computed(() => {
            const start = (currentPage.value - 1) * itemsPerPage.value
            const end = start + itemsPerPage.value
            return filteredDrinks.value.slice(start, end)
        })

        // Methods        
        const filterDrinks = () => {
            let results = allDrinks.value

            // Filter by search query
            if (searchQuery.value) {
                const query = searchQuery.value.toLowerCase()
                results = results.filter(drink =>
                    drink.name.toLowerCase().includes(query) ||
                    drink.description.toLowerCase().includes(query)
                )
            }

            // Filter by category
            if (selectedCategory.value) {
                results = results.filter(drink => drink.category === selectedCategory.value)
            }

            // Filter by price
            results = results.filter(drink => drink.price <= priceRange.value)

            filteredDrinks.value = results
            currentPage.value = 1 // Reset to first page with new filters
        }

        const resetFilters = () => {
            searchQuery.value = ''
            selectedCategory.value = ''
            priceRange.value = maxPrice.value
            filterDrinks()
        }

        const changePage = (page) => {
            currentPage.value = page
        }

        // Initialize
        onMounted(() => {
            // Set initial price range to max price
            priceRange.value = maxPrice.value
            filterDrinks()
        })

        const router = useRouter();

        const goToDrinkCustomization = (drinkId) => {
            router.push(`/drink/${drinkId}`);
        };

        return {
            searchQuery,
            selectedCategory,
            priceRange,
            allDrinks,
            filteredDrinks,
            categories,
            minPrice,
            maxPrice,
            currentPage,
            totalPages,
            paginatedDrinks,
            filterDrinks,
            resetFilters,
            changePage,
            goToDrinkCustomization
        }
    }
}
</script>

<style scoped>
.menu-container {
    background-color: var(--light);
    min-height: 100vh;
    padding-bottom: 4rem;
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

.menu-header {
    background-color: var(--primary);
    color: white;
    padding: 5rem 0 3rem;
    text-align: center;
    margin-bottom: 2rem;
}

.menu-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.menu-header p {
    font-size: 1.2rem;
    opacity: 0.8;
}

.menu-controls {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.search-box {
    position: relative;
    width: 100%;
}

.search-box input {
    width: 100%;
    padding: 1rem;
    padding-right: 3rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
}

.search-icon {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-light);
    cursor: pointer;
}

.filter-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    align-items: flex-end;
}

.filter-group {
    flex: 1;
    min-width: 200px;
}

.filter-group label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.filter-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    background-color: white;
}

.price-slider {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.price-slider input {
    flex: 1;
}

.price-slider span {
    font-weight: 600;
    color: var(--primary);
    min-width: 50px;
}

.reset-btn {
    background-color: var(--secondary);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.reset-btn:hover {
    background-color: var(--primary);
}

.drinks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    gap: 2rem;
}

.drink-card {
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.drink-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.drink-image {
    height: 200px;
    position: relative;
    overflow: hidden;
}

.drink-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s;
}

.drink-card:hover .drink-image img {
    transform: scale(1.05);
}

.featured-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background-color: var(--accent);
    color: var(--dark);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
}

.drink-info {
    padding: 1.5rem;
}

.drink-info h3 {
    margin-bottom: 0.5rem;
    color: var(--dark);
}

.drink-description {
    color: var(--text-light);
    font-size: 0.9rem;
    margin-bottom: 1rem;
    height: 2.7rem;
    /* Force uniform height for descriptions */
    overflow: hidden;
}

.drink-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.drink-category {
    background-color: var(--light);
    color: var(--primary);
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
}

.drink-price {
    font-weight: bold;
    font-size: 24px;
    color: var(--primary);
}

.add-to-cart-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.75rem 1rem;
    width: 50%;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.add-to-cart-btn:hover {
    background-color: var(--dark);
}

.no-results {
    text-align: center;
    padding: 3rem;
    color: var(--text-light);
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 3rem;
}

.page-btn {
    background-color: white;
    border: 1px solid #ddd;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s;
}

.page-btn:hover:not([disabled]) {
    background-color: var(--primary);
    color: white;
}

.page-btn[disabled] {
    opacity: 0.5;
    cursor: not-allowed;
}

.page-info {
    font-weight: 600;
    color: var(--text);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .menu-controls {
        gap: 1rem;
    }

    .filter-controls {
        flex-direction: column;
        gap: 1rem;
    }

    .filter-group {
        width: 100%;
    }

    .menu-header {
        padding: 4rem 0 2rem;
    }

    .menu-header h1 {
        font-size: 2rem;
    }
}
</style>