<template>
    <div class="profile-container" style="max-width: 1200px; margin: 0 auto; padding: 5rem 2rem;">
        <!-- Page Header with improved layout -->
        <div class="header-section" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div>
                <!-- <div class="section-heading">
                    <h2>My Account</h2>
                    <p>Manage your orders and personal information</p>
                </div> -->
                
                <!-- Back link -->
                <a href="http://localhost:5173/"
                    style="color: var(--primary); display: flex; align-items: center; text-decoration: none; font-weight: 500; margin-top: 0.5rem;">
                    <i class="fas fa-arrow-left" style="margin-right: 0.5rem;"></i> Back to Home
                </a>
            </div>
            
            <!-- Moved logout button to top-right -->
            <button @click="logout" style="background: none; border: 1px solid var(--primary); color: var(--primary); 
                           padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;
                           transition: all 0.3s; display: flex; align-items: center;">
                <i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>
                Logout
            </button>
        </div>

        <!-- Profile Tabs -->
        <div class="profile-tabs" style="margin-bottom: 2rem;">
            <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
                :class="{ active: activeTab === tab.id }"
                style="padding: 1rem 1.5rem; background: none; border: none; border-bottom: 3px solid transparent; margin-right: 1rem; font-weight: 500; cursor: pointer; position: relative; transition: color 0.3s, border-bottom-color 0.3s;"
                :style="activeTab === tab.id ? 'border-bottom-color: var(--accent); color: var(--dark);' : 'color: var(--text-light);'">
                <i :class="tab.icon" style="margin-right: 0.5rem;"></i>
                {{ tab.name }}

                <!-- Notification badge for current orders -->
                <span v-if="tab.id === 'current-orders' && currentOrders.length > 0"
                    style="position: absolute; top: 0.5rem; right: 0.3rem; background-color: var(--accent); color: var(--dark); border-radius: 50%; width: 20px; height: 20px; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; font-weight: bold;">
                    {{ currentOrders.length }}
                </span>
            </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content"
            style="background-color: white; border-radius: 10px; padding: 2rem; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
            <!-- Current Orders Tab -->
            <div v-if="activeTab === 'current-orders'">
                <h3 style="margin-bottom: 1.5rem; color: var(--primary); font-size: 1.5rem;">Current Orders</h3>

                <div v-if="currentOrders.length === 0" style="text-align: center; padding: 2rem 0;">
                    <i class="fas fa-shopping-bag"
                        style="font-size: 2.5rem; color: var(--secondary); margin-bottom: 1rem;"></i>
                    <p style="color: var(--text-light);">You don't have any ongoing orders</p>
                </div>

                <div v-else class="orders-list">
                    <div v-for="(order, index) in currentOrders" :key="order.id" class="order-card"
                        style="border: 1px solid #eee; border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; transition: transform 0.3s, box-shadow 0.3s;">
                        <!-- Order header -->
                        <div
                            style="padding: 1rem; background-color: var(--light); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                            <div>
                                <span style="font-weight: bold; color: var(--dark);">Order #{{ order.orderNumber
                                }}</span>
                                <span style="margin-left: 1rem; font-size: 0.9rem; color: var(--text-light);">{{
                                    order.date }}</span>
                            </div>
                            <div>
                                <span
                                    style="padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500;"
                                    :style="getStatusStyle(order.status)">
                                    {{ order.status }}
                                </span>
                            </div>
                        </div>

                        <!-- Order content -->
                        <div style="padding: 1rem;">
                            <div v-for="item in order.items" :key="item.id"
                                style="display: flex; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
                                <img :src="item.image" :alt="item.name"
                                    style="width: 60px; height: 60px; object-fit: cover; border-radius: 5px; margin-right: 1rem;">
                                <div style="flex-grow: 1;">
                                    <h4 style="margin-bottom: 0.3rem; color: var(--dark);">{{ item.name }}</h4>
                                    <p style="font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.5rem;">Qty:
                                        {{ item.quantity }}</p>
                                    <p style="font-weight: 500; color: var(--primary);">${{ item.price.toFixed(2) }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Order footer -->
                        <div
                            style="padding: 1rem; border-top: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background-color: var(--light);">
                            <div>
                                <span style="font-weight: bold; color: var(--primary);">Total: ${{
                                    order.total.toFixed(2) }}</span>
                            </div>
                            <div>
                                <button
                                    style="background: none; border: none; color: var(--primary); font-weight: 500; cursor: pointer; transition: color 0.3s;"
                                    @click="trackOrder(order.id)">
                                    Track Order
                                </button>
                                <button v-if="order.status === 'Processing' || order.status === 'Preparing'"
                                    style="background: none; border: none; color: var(--text-light); margin-left: 1rem; font-weight: 500; cursor: pointer; transition: color 0.3s;"
                                    @click="cancelOrder(order.id)">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Order History Tab -->
            <div v-if="activeTab === 'order-history'">
                <h3 style="margin-bottom: 1.5rem; color: var(--primary); font-size: 1.5rem;">Order History</h3>

                <div v-if="pastOrders.length === 0" style="text-align: center; padding: 2rem 0;">
                    <i class="fas fa-history"
                        style="font-size: 2.5rem; color: var(--secondary); margin-bottom: 1rem;"></i>
                    <p style="color: var(--text-light);">You don't have any past orders</p>
                </div>

                <div v-else class="orders-list">
                    <div v-for="(order, index) in pastOrders" :key="order.id" class="order-card"
                        style="border: 1px solid #eee; border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; transition: transform 0.3s, box-shadow 0.3s;">
                        <!-- Order header -->
                        <div
                            style="padding: 1rem; background-color: var(--light); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                            <div>
                                <span style="font-weight: bold; color: var(--dark);">Order #{{ order.orderNumber
                                }}</span>
                                <span style="margin-left: 1rem; font-size: 0.9rem; color: var(--text-light);">{{
                                    order.date }}</span>
                            </div>
                            <div>
                                <span
                                    style="padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; background-color: #E0E0E0; color: var(--text);">
                                    {{ order.status }}
                                </span>
                            </div>
                        </div>

                        <!-- Order content (collapsed by default) -->
                        <div v-if="expandedOrders.includes(order.id)" style="padding: 1rem;">
                            <div v-for="item in order.items" :key="item.id"
                                style="display: flex; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #eee;">
                                <img :src="item.image" :alt="item.name"
                                    style="width: 60px; height: 60px; object-fit: cover; border-radius: 5px; margin-right: 1rem;">
                                <div style="flex-grow: 1;">
                                    <h4 style="margin-bottom: 0.3rem; color: var(--dark);">{{ item.name }}</h4>
                                    <p style="font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.5rem;">Qty:
                                        {{ item.quantity }}</p>
                                    <p style="font-weight: 500; color: var(--primary);">${{ item.price.toFixed(2) }}</p>
                                </div>
                            </div>
                        </div>

                        <!-- Order footer -->
                        <div
                            style="padding: 1rem; border-top: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background-color: var(--light);">
                            <div>
                                <span style="font-weight: bold; color: var(--primary);">Total: ${{
                                    order.total.toFixed(2) }}</span>
                            </div>
                            <div style="display: flex; gap: 1rem;">
                                <button
                                    style="background: none; border: none; color: var(--primary); font-weight: 500; cursor: pointer; transition: color 0.3s;"
                                    @click="toggleOrderDetails(order.id)">
                                    {{ expandedOrders.includes(order.id) ? 'Hide Details' : 'View Details' }}
                                </button>
                                <button
                                    style="background: none; border: none; color: var(--primary); font-weight: 500; cursor: pointer; transition: color 0.3s;"
                                    @click="reorderItems(order.id)">
                                    Reorder
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Account Settings Tab -->
            <div v-if="activeTab === 'account-settings'">
                <h3 style="margin-bottom: 1.5rem; color: var(--primary); font-size: 1.5rem;">Account Settings</h3>

                <form @submit.prevent="saveAccountSettings">
                    <!-- Personal Information Section -->
                    <div style="margin-bottom: 2rem;">
                        <h4 style="margin-bottom: 1rem; color: var(--dark); font-size: 1.1rem;">Personal Information
                        </h4>

                        <div
                            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                            <div>
                                <label for="firstName"
                                    style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">First
                                    Name</label>
                                <input id="firstName" v-model="userProfile.firstName" type="text"
                                    style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;"
                                    required>
                            </div>

                            <div>
                                <label for="lastName"
                                    style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">Last
                                    Name</label>
                                <input id="lastName" v-model="userProfile.lastName" type="text"
                                    style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;"
                                    required>
                            </div>
                        </div>

                        <div style="margin-bottom: 1rem;">
                            <label for="email"
                                style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">Email
                                Address</label>
                            <input id="email" v-model="userProfile.email" type="email"
                                style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;"
                                required>
                        </div>

                        <div>
                            <label for="phone"
                                style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">Phone
                                Number</label>
                            <input id="phone" v-model="userProfile.phone" type="tel"
                                style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;">
                        </div>
                    </div>

                    <!-- Password Section -->
                    <div style="margin-bottom: 2rem;">
                        <h4 style="margin-bottom: 1rem; color: var(--dark); font-size: 1.1rem;">Change Password</h4>

                        <div style="margin-bottom: 1rem;">
                            <label for="currentPassword"
                                style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">Current
                                Password</label>
                            <input id="currentPassword" v-model="passwordChange.current" type="password"
                                style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;">
                        </div>

                        <div
                            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                            <div>
                                <label for="newPassword"
                                    style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">New
                                    Password</label>
                                <input id="newPassword" v-model="passwordChange.new" type="password"
                                    style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;">
                            </div>

                            <div>
                                <label for="confirmPassword"
                                    style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: var(--text);">Confirm
                                    New
                                    Password</label>
                                <input id="confirmPassword" v-model="passwordChange.confirm" type="password"
                                    style="width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 5px; outline: none; transition: border-color 0.3s;">
                            </div>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <div style="display: flex; justify-content: flex-end;">
                        <button type="submit"
                            style="background-color: var(--accent); color: var(--dark); border: none; padding: 0.8rem 2rem; border-radius: 5px; font-weight: bold; cursor: pointer; transition: background-color 0.3s, transform 0.2s;">
                            Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '../authStore';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import axios from 'axios';

export default {
    setup() {
        const authStore = useAuthStore();
        return { authStore };
    },
    data() {
        return {
            activeTab: 'current-orders',
            tabs: [
                { id: 'current-orders', name: 'Current Orders', icon: 'fas fa-shopping-bag' },
                { id: 'order-history', name: 'Order History', icon: 'fas fa-history' },
                { id: 'account-settings', name: 'Account Settings', icon: 'fas fa-user-cog' }
            ],
            currentOrders: [/* your order data */],
            pastOrders: [/* your past order data */],
            expandedOrders: [],
            userProfile: {
                firstName: '',
                lastName: '',
                email: '',
                phone: '',
                address: {
                    line1: '',
                    line2: '',
                    city: '',
                    state: '',
                    zip: ''
                },
                preferences: {
                    newsletter: false,
                    textNotifications: false
                }
            },
            passwordChange: {
                current: '',
                new: '',
                confirm: ''
            }
        };
    },

    mounted() {
        const auth = getAuth();
        onAuthStateChanged(auth, (user) => {
            if (user) {
                this.fetchUserProfile(user);
            } else {
                console.warn("User not logged in.");
                this.$router.push('/login'); // optional redirect
            }
        })
        
                
    },

    methods: {
        async fetchUserProfile(user) {
            try {
                const idToken = await user.getIdToken();
                const res = await axios.get("http://localhost:5019/profile", {
                    headers: {
                        Authorization: idToken
                    }
                });

                const profile = res.data;
                const [firstName, ...lastNameParts] = profile.userName.split(" ");
                const lastName = lastNameParts.join(" ");

                this.userProfile.firstName = firstName;
                this.userProfile.lastName = lastName;
                this.userProfile.email = profile.email;
                this.userProfile.phone = profile.phoneNum;

            } catch (error) {
                console.error("Failed to fetch profile:", error);
            }
        },

        async updateProfile() {
            try {
                const auth = getAuth();
                const currentUser = auth.currentUser;

                if (!currentUser) {
                    alert("User not logged in.");
                    return;
                }

                const idToken = await currentUser.getIdToken();
                const userId = currentUser.uid;
                const fullName = `${this.userProfile.firstName} ${this.userProfile.lastName}`;

                await axios.put(`http://localhost:5018/update_profile/${userId}`, {
                    email: this.userProfile.email,
                    phoneNum: this.userProfile.phone,
                    userName: fullName
                }, {
                    headers: {
                        Authorization: idToken
                    }
                });

                alert("Profile updated successfully!");

            } catch (error) {
                console.error("Profile update failed:", error);
                alert("Failed to update profile. Please try again.");
            }
        },

        async saveAccountSettings() {
            if (this.passwordChange.current && this.passwordChange.new) {
                if (this.passwordChange.new !== this.passwordChange.confirm) {
                    alert('New passwords do not match');
                    return;
                }

                alert('Password updated successfully (mock)');
                this.passwordChange.current = '';
                this.passwordChange.new = '';
                this.passwordChange.confirm = '';
            }

            await this.updateProfile();
        },

        getStatusStyle(status) {
            switch (status) {
                case 'Processing':
                    return 'background-color: #FFF3CD; color: #856404;';
                case 'Preparing':
                    return 'background-color: #D1ECF1; color: #37546e;';
                case 'Completed':
                    return 'background-color: #daf2ea; color: #657a62;';
                case 'Collected':
                    return 'background-color: #D4EDDA; color: #155724;';
                case 'Cancelled':
                    return 'background-color: #F8D7DA; color: #721C24;';
                default:
                    return 'background-color: #E2E3E5; color: #383D41;';
            }
        },

        toggleOrderDetails(orderId) {
            if (this.expandedOrders.includes(orderId)) {
                this.expandedOrders = this.expandedOrders.filter(id => id !== orderId);
            } else {
                this.expandedOrders.push(orderId);
            }
        },

        trackOrder(orderId) {
            alert(`Tracking order #${orderId}`);
        },

        cancelOrder(orderId) {
            if (confirm('Are you sure you want to cancel this order?')) {
                alert(`Order #${orderId} has been cancelled`);
                const orderIndex = this.currentOrders.findIndex(order => order.id === orderId);
                if (orderIndex !== -1) {
                    this.currentOrders[orderIndex].status = 'Cancelled';
                    this.pastOrders.unshift(this.currentOrders[orderIndex]);
                    this.currentOrders.splice(orderIndex, 1);
                }
            }
        },

        reorderItems(orderId) {
            alert(`Adding items from order #${orderId} to your cart`);
        },

        async logout() {
            try {
                await this.authStore.logout();
                this.$router.push('/'); // Redirect to login page after logout
            } catch (error) {
                console.error('Logout failed:', error);
                alert('Failed to logout. Please try again.');
            }
        },
    }
};
</script>

<style>
/* Order card hover effect */
.order-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

/* Input focus styles */
input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(93, 64, 55, 0.1);
}

/* Button hover effects */
button[type="submit"]:hover {
    background-color: #FFD54F;
    transform: translateY(-2px);
}

.tab-content button:hover {
    color: var(--accent) !important;
}

/* Logout button hover effect */
button[type="submit"]:hover, button[type="button"]:hover {
    transform: translateY(-2px);
}

/* Mobile-specific CSS */
@media (max-width: 768px) {
    .profile-tabs {
        display: flex;
        overflow-x: auto;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }

    .profile-tabs button {
        flex: 0 0 auto;
        white-space: nowrap;
        padding: 0.8rem 1rem;
        margin-right: 0.5rem;
        font-size: 0.9rem;
    }

    .tab-content {
        padding: 1.5rem;
    }

    .section-heading h2 {
        font-size: 1.8rem;
    }

    .profile-container {
        padding: 4rem 1rem 2rem;
    }
    
    /* Responsive header for mobile */
    .header-section {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .header-section button {
        margin-top: 1rem;
        align-self: flex-start;
    }
}
</style>