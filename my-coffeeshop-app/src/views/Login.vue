<script setup>
import { ref } from 'vue';
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile, signInWithPopup, sendPasswordResetEmail } from 'firebase/auth';

const firebaseConfig = {
    apiKey: "AIzaSyCvIDqbUMswOpiUuhK4T5F1xDtV6TF3DhY",
    authDomain: "esd-coffeehouse.firebaseapp.com",
    projectId: "esd-coffeehouse",
    storageBucket: "esd-coffeehouse.firebasestorage.app",
    messagingSenderId: "775228208734",
    appId: "1:775228208734:web:e789da4fb8fd39b6d6e6cf",
    measurementId: "G-6Q5J1S1KLP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

// State variables
const activeTab = ref('login');
const errorMessage = ref('');
const successMessage = ref('');

const loginForm = ref({
    email: '',
    password: ''
});

const registerForm = ref({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
});

// Methods
const login = async () => {
    try {
        errorMessage.value = '';
        successMessage.value = '';

        await signInWithEmailAndPassword(
            auth,
            loginForm.value.email,
            loginForm.value.password
        );

        successMessage.value = 'Login successful! Redirecting...';
        setTimeout(() => {
            window.location.href = "../BrewHaven/profile.html";
        }, 1500);
    } catch (error) {
        errorMessage.value = error.message;
    }
};

const register = async () => {
    try {
        errorMessage.value = '';
        successMessage.value = '';

        if (registerForm.value.password !== registerForm.value.confirmPassword) {
            errorMessage.value = 'Passwords do not match';
            return;
        }

        // Create user
        const userCredential = await createUserWithEmailAndPassword(
            auth,
            registerForm.value.email,
            registerForm.value.password
        );

        // Update profile with name
        await updateProfile(userCredential.user, {
            displayName: registerForm.value.name
        });

        successMessage.value = 'Account created successfully! You can now log in.';
        activeTab.value = 'login';
    } catch (error) {
        errorMessage.value = error.message;
    }
};

const loginWithGoogle = async () => {
    try {
        errorMessage.value = '';
        successMessage.value = '';

        await signInWithPopup(auth, googleProvider);

        successMessage.value = 'Login successful! Redirecting...';
        setTimeout(() => {
            window.location.href = '/dashboard.html';
        }, 1500);
    } catch (error) {
        errorMessage.value = error.message;
    }
};

const forgotPassword = async () => {
    try {
        errorMessage.value = '';
        successMessage.value = '';

        if (!loginForm.value.email) {
            errorMessage.value = 'Please enter your email address';
            return;
        }

        await sendPasswordResetEmail(auth, loginForm.value.email);
        successMessage.value = 'Password reset email sent! Check your inbox.';
    } catch (error) {
        errorMessage.value = error.message;
    }
};
</script>

<template>
    <div class="logo">
        <h1>☕</h1>
        <h1>Brew Heaven</h1>
        <br>
        <p>Creating Perfect Memories</p>
    </div>

    <div class="card">
        <div class="tabs">
            <div class="tab" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">
                Login
            </div>
            <div class="tab" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">
                Create Account
            </div>
        </div>

        <div v-if="activeTab === 'login'">
            <form @submit.prevent="login">
                <div class="form-group">
                    <label for="login-email">Email</label>
                    <input type="email" id="login-email" v-model="loginForm.email" required
                        placeholder="your@email.com">
                </div>

                <div class="form-group">
                    <label for="login-password">Password</label>
                    <input type="password" id="login-password" v-model="loginForm.password" required
                        placeholder="Enter your password">
                </div>

                <button type="submit" class="btn btn-primary">
                    Log In
                </button>
            </form>

            <div class="forgot-password">
                <a href="#" @click.prevent="forgotPassword">Forgot Password?</a>
            </div>

            <button @click="loginWithGoogle" class="btn btn-google">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google Logo">
                Continue with Google
            </button>
        </div>

        <div v-if="activeTab === 'register'">
            <form @submit.prevent="register">
                <div class="form-group">
                    <label for="register-name">Full Name</label>
                    <input type="text" id="register-name" v-model="registerForm.name" required placeholder="Your name">
                </div>

                <div class="form-group">
                    <label for="register-email">Email</label>
                    <input type="email" id="register-email" v-model="registerForm.email" required
                        placeholder="your@email.com">
                </div>

                <div class="form-group">
                    <label for="register-password">Password</label>
                    <input type="password" id="register-password" v-model="registerForm.password" required
                        placeholder="Create a password">
                </div>

                <div class="form-group">
                    <label for="register-confirm-password">Confirm Password</label>
                    <input type="password" id="register-confirm-password" v-model="registerForm.confirmPassword"
                        required placeholder="Confirm your password">
                </div>

                <button type="submit" class="btn btn-primary">
                    Create Account
                </button>
            </form>

            <button @click="loginWithGoogle" class="btn btn-google">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google Logo">
                Sign Up with Google
            </button>
        </div>

        <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="success-message">
            {{ successMessage }}
        </div>
    </div>
</template>

<style>
.container {
    width: 100%;
    max-width: 600px; /* Adjust as needed */
    padding: 2rem;
    margin: 0 auto; /* Center the container */
}
.logo {
    text-align: center;
    margin-bottom: 2rem;
}

.logo h1 {
    font-size: 2.5rem;
    color: #6f4e37;
    margin-bottom: 0.5rem;
}

.logo p {
    color: #8c7b67;
}

.card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.tabs {
    display: flex;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #e0d8cf;
}

.tab {
    flex: 1;
    text-align: center;
    padding: 0.75rem;
    cursor: pointer;
    font-weight: 600;
    color: #8c7b67;
    transition: all 0.3s ease;
}

.tab.active {
    color: #6f4e37;
    border-bottom: 3px solid #6f4e37;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e0d8cf;
    border-radius: 6px;
    font-size: 1rem;
    transition: border 0.3s ease;
}

.form-group input:focus {
    outline: none;
    border-color: #6f4e37;
}

.btn {
    width: 100%;
    padding: 0.85rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color: #6f4e37;
    color: white;
}

.btn-primary:hover {
    background-color: #5d412e;
}

.btn-google {
    background-color: white;
    border: 1px solid #e0d8cf;
    color: #4a3520;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 1rem;
}

.btn-google:hover {
    background-color: #f8f8f8;
}

.btn-google img {
    width: 20px;
    margin-right: 10px;
}

.forgot-password {
    text-align: center;
    margin-top: 1rem;
}

.forgot-password a {
    color: #8c7b67;
    text-decoration: none;
}

.forgot-password a:hover {
    color: #6f4e37;
    text-decoration: underline;
}

.error-message {
    color: #e74c3c;
    margin-top: 1rem;
    text-align: center;
}

.success-message {
    color: #27ae60;
    margin-top: 1rem;
    text-align: center;
}
</style>