<template>
    <div class="profile-container">
        <!-- Loading state -->
        <div v-if="authStore.isLoading" class="loading-state">
            Loading profile...
        </div>

        <!-- Error state -->
        <div v-else-if="authStore.error" class="error-state">
            Error: {{ authStore.error }}
        </div>

        <!-- Main content when data is loaded -->
        <template v-else>
            <!-- Profile Sidebar -->
            <div class="profile-sidebar">
                <div class="profile-photo">
                    <span>{{ getUserInitials() }}</span>
                </div>
                <h2 class="profile-name">{{ authStore.userFullName }}</h2>
                <p class="profile-email">{{ authStore.user?.email }}</p>

                <ul class="sidebar-menu">
                    <li v-for="tab in tabs" :key="tab.id">
                        <a href="#" :class="{ active: activeTab === tab.id }" @click.prevent="setActiveTab(tab.id)">
                            {{ tab.label }}
                        </a>
                    </li>
                </ul>

                <!-- Logout Button -->
                <div class="logout-container">
                    <button class="btn-logout" @click="logout">
                        Logout
                    </button>
                </div>
            </div>

            <!-- Content Area -->
            <div class="content-area">
                <!-- Profile Tab -->
                <div v-if="activeTab === 'profile'" class="content-tab">
                    <div class="content-header">
                        <h2 class="content-title">Profile Information</h2>
                    </div>

                    <div class="profile-info">
                        <div>
                            <div class="info-item">
                                <div class="info-label">First Name</div>
                                <div class="info-value">{{ authStore.userProfile?.firstName }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Last Name</div>
                                <div class="info-value">{{ authStore.userProfile?.lastName }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Email</div>
                                <div class="info-value">{{ authStore.user?.email }}</div>
                            </div>
                        </div>
                        <div>
                            <div class="info-item">
                                <div class="info-label">Phone Number</div>
                                <div class="info-value">{{ authStore.userProfile?.phoneNumber }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Auth Provider</div>
                                <div class="info-value">{{ authStore.userProfile?.authProvider }}</div>
                            </div>
                            <div class="info-item">
                                <div class="info-label">Account Created</div>
                                <div class="info-value">{{ formatDate(authStore.userProfile?.createdAt) }}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Ongoing Orders Tab -->
                <div v-if="activeTab === 'ongoing'" class="content-tab">
                    <div class="content-header">
                        <h2 class="content-title">Ongoing Orders</h2>
                    </div>

                    <div v-if="isLoadingOrders" class="loading-state">
                        Loading your orders...
                    </div>

                    <div v-else-if="ordersError" class="error-state">
                        Error loading orders: {{ ordersError }}
                        <button class="btn btn-secondary" @click="fetchOrders">Try Again</button>
                    </div>

                    <div v-else-if="ongoingOrders.length === 0" class="empty-state">
                        <p>You don't have any ongoing orders at the moment.</p>
                    </div>

                    <div v-else class="order-list">
                        <div v-for="order in ongoingOrders" :key="order.id" class="order-card">
                            <div class="order-header">
                                <span class="order-id">Order #{{ order.id }}</span>
                                <span class="order-date">{{ formatDate(order.date) }}</span>
                            </div>
                            <div class="order-outlet">{{ order.outletName }}</div>
                            <div class="order-status status-processing">{{ order.status }}</div>
                            <div class="order-items">
                                <p v-for="(item, index) in order.items" :key="index">
                                    {{ item.quantity }}x {{ item.name }} - ${{ item.price }} each
                                    <span v-if="item.customizations && item.customizations.length > 0" class="customizations">
                                        <br>
                                        <span class="customization-title">Customizations:</span>
                                        <span v-for="(cust, cIndex) in item.customizations" :key="cIndex" class="customization-item">
                                            {{ cust.name }} ({{ cust.type }})
                                            <span v-if="cust.price_diff > 0">+${{ cust.price_diff }}</span>
                                            <span v-else-if="cust.price_diff < 0">-${{ Math.abs(cust.price_diff) }}</span>
                                        </span>
                                    </span>
                                </p>
                            </div>
                            <div class="order-footer">
                                <div class="order-total">Total: ${{ order.total.toFixed(2) }}</div>
                                <button class="btn btn-secondary" @click="trackOrder(order.id)">Track Order</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Past Orders Tab -->
                <div v-if="activeTab === 'past'" class="content-tab">
                    <div class="content-header">
                        <h2 class="content-title">Past Orders</h2>
                    </div>

                    <div v-if="isLoadingOrders" class="loading-state">
                        Loading your orders...
                    </div>

                    <div v-else-if="ordersError" class="error-state">
                        Error loading orders: {{ ordersError }}
                        <button class="btn btn-secondary" @click="fetchOrders">Try Again</button>
                    </div>

                    <div v-else-if="pastOrders.length === 0" class="empty-state">
                        <p>You don't have any past orders yet.</p>
                    </div>

                    <div v-else class="order-list">
                        <div v-for="order in pastOrders" :key="order.id" class="order-card">
                            <div class="order-header">
                                <span class="order-id">Order #{{ order.id }}</span>
                                <span class="order-date">{{ formatDate(order.date) }}</span>
                            </div>
                            <div class="order-outlet">{{ order.outletName }}</div>
                            <div class="order-status" :class="order.status.toLowerCase() === 'completed' ? 'status-completed' : 'status-cancelled'">
                                {{ order.status }}
                            </div>
                            <div class="order-items">
                                <p v-for="(item, index) in order.items" :key="index">
                                    {{ item.quantity }}x {{ item.name }} - ${{ item.price }} each
                                    <span v-if="item.customizations && item.customizations.length > 0" class="customizations">
                                        <br>
                                        <span class="customization-title">Customizations:</span>
                                        <span v-for="(cust, cIndex) in item.customizations" :key="cIndex" class="customization-item">
                                            {{ cust.name }} ({{ cust.type }})
                                            <span v-if="cust.price_diff > 0">+${{ cust.price_diff }}</span>
                                            <span v-else-if="cust.price_diff < 0">-${{ Math.abs(cust.price_diff) }}</span>
                                        </span>
                                    </span>
                                </p>
                            </div>
                            <div class="order-footer">
                                <div class="order-total">Total: ${{ order.total.toFixed(2) }}</div>
                                <button class="btn btn-secondary" @click="viewOrderDetails(order.id)">View Details</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Edit Profile Tab -->
                <div v-if="activeTab === 'edit'" class="content-tab">
                    <div class="content-header">
                        <h2 class="content-title">Edit Profile</h2>
                    </div>

                    <form @submit.prevent="updateProfile">
                        <div class="form-group">
                            <label class="form-label" for="firstName">First Name</label>
                            <input type="text" id="firstName" class="form-control" v-model="formData.firstName">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="lastName">Last Name</label>
                            <input type="text" id="lastName" class="form-control" v-model="formData.lastName">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="email">Email</label>
                            <input type="email" id="email" class="form-control" v-model="formData.email" disabled>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="phone">Phone Number</label>
                            <input type="tel" id="phone" class="form-control" v-model="formData.phoneNumber">
                        </div>

                        <div class="form-actions">
                            <button type="button" class="btn btn-secondary" @click="cancelEdit">Cancel</button>
                            <button type="submit" class="btn">Save Changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import { useAuthStore } from '../authStore';
import { ref, onMounted, computed } from 'vue';
import { getFirestore, doc, updateDoc } from 'firebase/firestore';
import { useRouter } from 'vue-router';
import axios from 'axios'; // Make sure axios is installed

export default {
    name: 'UserProfile',
    setup() {
        const authStore = useAuthStore();
        const router = useRouter();
        const activeTab = ref('profile');
        const formData = ref({
            firstName: '',
            lastName: '',
            email: '',
            phoneNumber: ''
        });

        // Replace demo data with real data containers
        const orders = ref([]);
        const isLoadingOrders = ref(false);
        const ordersError = ref(null);

        // Computed properties to filter orders by status
        const ongoingOrders = computed(() => {
            return orders.value.filter(order => 
                order.status && ['PENDING', 'PROCESSING', 'READY'].includes(order.status.toUpperCase())
            );
        });

        const pastOrders = computed(() => {
            return orders.value.filter(order => 
                order.status && ['COMPLETED', 'CANCELLED'].includes(order.status.toUpperCase())
            );
        });

        const tabs = [
            { id: 'profile', label: 'Profile' },
            { id: 'ongoing', label: 'Ongoing Orders' },
            { id: 'past', label: 'Past Orders' },
            { id: 'edit', label: 'Edit Profile' }
        ];

        // Function to fetch orders from API
        const fetchOrders = async () => {
            if (!authStore.user?.uid) return;
            
            isLoadingOrders.value = true;
            ordersError.value = null;
            
            try {
                // Using the user ID from auth store to fetch orders
                const response = await axios.get(`http://localhost:5201/get_orders_by_user/${authStore.user.uid}`);
                
                if (response.data && response.data.code === 200 && response.data.data) {
                    // Process the orders data
                    orders.value = response.data.data.orders.map(order => ({
                        id: order.order_id,
                        date: order.date_created,
                        status: order.status,
                        outletName: order.outlet_name?.name || 'Unknown Location',
                        items: order.items.map(item => ({
                            name: item.drink_name,
                            price: item.drink_price,
                            quantity: item.quantity,
                            customizations: item.customizations
                        })),
                        total: order.total_price
                    }));
                } else {
                    ordersError.value = 'Failed to fetch orders data';
                }
            } catch (error) {
                console.error('Error fetching orders:', error);
                ordersError.value = error.message || 'Failed to fetch orders';
            } finally {
                isLoadingOrders.value = false;
            }
        };

        const resetFormData = () => {
            formData.value = {
                firstName: authStore.userProfile?.firstName || '',
                lastName: authStore.userProfile?.lastName || '',
                email: authStore.user?.email || '',
                phoneNumber: authStore.userProfile?.phoneNumber || ''
            };
        };

        onMounted(async () => {
            await authStore.init();
            resetFormData();
            fetchOrders(); // Fetch orders when component mounts
        });

        const getUserInitials = () => {
            if (!authStore.userProfile) return '';
            return `${authStore.userProfile.firstName?.charAt(0) || ''}${authStore.userProfile.lastName?.charAt(0) || ''}`;
        };

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            }).format(date);
        };

        const updateProfile = async () => {
            try {
                const db = getFirestore();
                await updateDoc(doc(db, 'users', authStore.user.uid), {
                    firstName: formData.value.firstName,
                    lastName: formData.value.lastName,
                    phoneNumber: formData.value.phoneNumber
                });

                await authStore.init();
                activeTab.value = 'profile';
                alert('Profile updated successfully!');
            } catch (error) {
                console.error('Error updating profile:', error);
                alert('Failed to update profile');
            }
        };

        const logout = async () => {
            try {
                await authStore.logout();
                router.push('/'); // Redirect to homepage after successful logout
            } catch (error) {
                console.error('Logout error:', error);
            }
        };

        const viewOrderDetails = async (orderId) => {
            try {
                const response = await axios.get(`http://localhost:5201/get_order_details/${authStore.user.uid}/${orderId}`);
                if (response.data && response.data.code === 200) {
                    // Navigate to order details or show in modal
                    console.log(`Viewing details for order: ${orderId}`);
                    // Optionally navigate to a detailed view
                    // router.push(`/order/${orderId}`);
                }
            } catch (error) {
                console.error(`Error fetching order details for ${orderId}:`, error);
                alert('Failed to load order details');
            }
        };

        return {
            authStore,
            activeTab,
            tabs,
            formData,
            ongoingOrders,
            pastOrders,
            isLoadingOrders,
            ordersError,
            getUserInitials,
            formatDate,
            resetFormData,
            updateProfile,
            logout,
            fetchOrders,
            setActiveTab: (tabId) => { 
                activeTab.value = tabId; 
                // Refresh orders data when switching to order tabs
                if (tabId === 'ongoing' || tabId === 'past') {
                    fetchOrders();
                }
            },
            cancelEdit: () => {
                resetFormData();
                activeTab.value = 'profile';
            },
            trackOrder: (orderId) => {
                console.log(`Tracking order: ${orderId}`);
                router.push(`/trackOrders/${orderId}`);
            },
            viewOrderDetails
        };
    }
};
</script>

<style scoped>
.profile-container {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 30px;
    max-width: 1200px;
    margin: 10rem auto;
    padding: 0 2rem;
}

.profile-sidebar {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    height: fit-content;
    display: flex;
    flex-direction: column;
}

.profile-photo {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background-color: var(--primary);
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1.5rem;
    font-size: 2.5rem;
    color: white;
}

.profile-name {
    text-align: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: var(--dark);
}

.profile-email {
    text-align: center;
    color: var(--text-light);
    margin-bottom: 2rem;
}

.sidebar-menu {
    list-style: none;
}

.sidebar-menu li {
    margin-bottom: 0.8rem;
}

.sidebar-menu a {
    display: block;
    padding: 0.8rem 1rem;
    text-decoration: none;
    color: var(--text);
    border-radius: 5px;
    transition: background-color 0.3s;
}

.sidebar-menu a:hover,
.sidebar-menu a.active {
    background-color: var(--light);
}

.sidebar-menu a.active {
    font-weight: bold;
    color: var(--primary);
}

/* Logout Button Styles */
.logout-container {
    margin-top: auto;
    padding-top: 2rem;
    border-top: 1px solid var(--light);
    margin-top: 2rem;
}

.btn-logout {
    width: 100%;
    padding: 0.8rem;
    background-color: var(--primary);
    color: var(--light);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: background-color 0.3s;
}

.btn-logout:hover {
    background-color: var(--secondary);
}

.content-area {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    padding: 2rem;
}

.content-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}

.content-title {
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--primary);
}

.profile-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin-bottom: 2rem;
}

.info-item {
    margin-bottom: 1.5rem;
}

.info-label {
    font-size: 0.9rem;
    color: var(--text-light);
    margin-bottom: 0.3rem;
}

.info-value {
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text);
}

.order-list {
    margin-top: 1.5rem;
}

.order-card {
    border: 1px solid var(--light);
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.3s;
}

.order-card:hover {
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.order-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.8rem;
}

.order-id {
    font-weight: bold;
    color: var(--dark);
}

.order-date {
    color: var(--text-light);
}

.order-outlet {
    font-weight: 500;
    color: var(--primary);
    margin-bottom: 0.7rem;
    font-size: 1.05rem;
}

.order-status {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.status-completed {
    background-color: #e6f4ea;
    color: #34a853;
}

.status-processing {
    background-color: #fef7e0;
    color: var(--accent);
}

.status-cancelled {
    background-color: #feeaea;
    color: #e53935;
}

.order-items {
    margin: 1rem 0;
    color: var(--text-light);
}

.order-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--light);
    padding-top: 1rem;
}

.order-total {
    font-weight: bold;
    font-size: 1.2rem;
    color: var(--primary);
}

.btn {
    padding: 0.7rem 1.2rem;
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 0.9rem;
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

.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--dark);
}

.form-control {
    width: 100%;
    padding: 0.8rem 1rem;
    border: 1px solid var(--light);
    border-radius: 5px;
    font-size: 1rem;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary);
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 2rem;
}

.empty-state {
    text-align: center;
    padding: 3rem 0;
    color: var(--text-light);
}

.loading-state, .error-state {
    text-align: center;
    padding: 3rem 0;
    color: var(--text-light);
}

.error-state {
    color: #d32f2f;
}

.customizations {
    display: block;
    margin-left: 1rem;
    font-size: 0.9rem;
    color: var(--text-light);
}

.customization-title {
    font-weight: 500;
    margin-right: 0.5rem;
}

.customization-item {
    display: inline-block;
    margin-right: 0.8rem;
}

@media (max-width: 768px) {
    .profile-container {
        grid-template-columns: 1fr;
    }

    .profile-info {
        grid-template-columns: 1fr;
    }
}
</style>