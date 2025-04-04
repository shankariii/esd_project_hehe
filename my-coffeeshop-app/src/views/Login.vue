<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="login-logo">
          <!-- <img src="../assets/Brew_Haven_Logo.png" alt="Coffee Shop Logo" /> -->
          <h1>☕ Brew Haven</h1>
        </div>
        <p class="login-tagline">Sign in to order your favorite brew</p>
      </div>

      <div class="login-tabs">
        <button 
          :class="['tab-btn', { active: activeTab === 'login' }]" 
          @click="activeTab = 'login'"
          :disabled="isLoading || activeTab === 'additional-info'"
        >
          Login
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'signup' }]" 
          @click="activeTab = 'signup'"
          :disabled="isLoading || activeTab === 'additional-info'"
        >
          Sign Up
        </button>
      </div>

      <!-- Login Form -->
      <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="loginForm.email" 
            required 
            placeholder="your@email.com"
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="loginForm.password" 
            required 
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>Login</span>
          </button>
          <a href="#" class="forgot-password" @click.prevent="forgotPassword" :class="{ disabled: isLoading }">Forgot Password?</a>
        </div>
        <div class="separator">
          <span>OR</span>
        </div>
        <button type="button" class="btn-google" @click="signInWithGoogle" :disabled="isLoading">
          <div class="google-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
          </div>
          <span v-if="isGoogleLoading" class="spinner"></span>
          <span v-else>Continue with Google</span>
        </button>
      </form>

      <!-- Sign Up Form -->
      <form v-if="activeTab === 'signup'" @submit.prevent="handleSignup" class="login-form">
        <div class="form-row">
          <div class="form-group">
            <label for="firstName">First Name</label>
            <input 
              type="text" 
              id="firstName" 
              v-model="signupForm.firstName" 
              required 
              placeholder="John"
              :disabled="isLoading"
            />
          </div>
          <div class="form-group">
            <label for="lastName">Last Name</label>
            <input 
              type="text" 
              id="lastName" 
              v-model="signupForm.lastName" 
              required 
              placeholder="Doe"
              :disabled="isLoading"
            />
          </div>
        </div>
        <div class="form-group">
          <label for="signupEmail">Email</label>
          <input 
            type="email" 
            id="signupEmail" 
            v-model="signupForm.email" 
            required 
            placeholder="your@email.com"
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="phoneNumber">Phone Number</label>
          <input 
            type="tel" 
            id="phoneNumber" 
            v-model="signupForm.phoneNumber" 
            required 
            placeholder="+1 (555) 123-4567"
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="signupPassword">Password</label>
          <input 
            type="password" 
            id="signupPassword" 
            v-model="signupForm.password" 
            required 
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="signupForm.confirmPassword" 
            required 
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>Create Account</span>
          </button>
        </div>
        <div class="separator">
          <span>OR</span>
        </div>
        <button type="button" class="btn-google" @click="signInWithGoogle" :disabled="isLoading">
          <div class="google-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
          </div>
          <span v-if="isGoogleLoading" class="spinner"></span>
          <span v-else>Continue with Google</span>
        </button>
      </form>

      <!-- Additional Info Form (for Google Auth users) -->
      <form v-if="activeTab === 'additional-info'" @submit.prevent="completeGoogleSignup" class="login-form">
        <h2>Complete Your Profile</h2>
        <p class="info-text">Please provide the following additional information to complete your registration.</p>
        
        <div class="form-group">
          <label for="googleFirstName">First Name</label>
          <input 
            type="text" 
            id="googleFirstName" 
            v-model="googleAuthForm.firstName" 
            required 
            :placeholder="googleAuthForm.firstName || 'First Name'"
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="googleLastName">Last Name</label>
          <input 
            type="text" 
            id="googleLastName" 
            v-model="googleAuthForm.lastName" 
            required 
            :placeholder="googleAuthForm.lastName || 'Last Name'"
            :disabled="isLoading"
          />
        </div>
        <div class="form-group">
          <label for="googlePhoneNumber">Phone Number</label>
          <input 
            type="tel" 
            id="googlePhoneNumber" 
            v-model="googleAuthForm.phoneNumber" 
            required 
            placeholder="+1 (555) 123-4567"
            :disabled="isLoading"
          />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="isLoading">
            <span v-if="isLoading" class="spinner"></span>
            <span v-else>Complete Registration</span>
          </button>
        </div>
      </form>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div v-if="success" class="success-message">
        {{ success }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, 
         signInWithPopup, GoogleAuthProvider, sendPasswordResetEmail } from 'firebase/auth';
import { getFirestore, doc, setDoc, getDoc, updateDoc } from 'firebase/firestore';
import { useAuthStore } from '../authStore'; // Import the auth store
import { useRouter } from 'vue-router'; // Import router for navigation

export default {
  name: 'LoginPage',
  setup() {
    const activeTab = ref('login');
    const error = ref('');
    const success = ref('');
    const isLoading = ref(false);
    const isGoogleLoading = ref(false);
    
    // Get the auth store and router
    const authStore = useAuthStore();
    const router = useRouter();
    
    const loginForm = reactive({
      email: '',
      password: ''
    });
    
    const signupForm = reactive({
      firstName: '',
      lastName: '',
      email: '',
      phoneNumber: '',
      password: '',
      confirmPassword: ''
    });
    
    const googleAuthForm = reactive({
      uid: '',
      email: '',
      firstName: '',
      lastName: '',
      phoneNumber: ''
    });
    
    const auth = getAuth();
    const db = getFirestore();
    const googleProvider = new GoogleAuthProvider();
    
    // Regular login with email/password
    const handleLogin = async () => {
      try {
        error.value = '';
        success.value = '';
        isLoading.value = true;
        
        const userCredential = await signInWithEmailAndPassword(
          auth, 
          loginForm.email, 
          loginForm.password
        );
        
        success.value = 'Login successful! Redirecting...';
        
        // Wait for auth store to update
        await authStore.init();
        
        // Redirect to main app after successful login
        setTimeout(() => {
          router.push('/findOutlet');
        }, 1000);
        
      } catch (err) {
        error.value = translateFirebaseError(err.code) || 'Failed to login. Please try again.';
      } finally {
        isLoading.value = false;
      }
    };
    
    // Sign up with email/password
    const handleSignup = async () => {
      try {
        error.value = '';
        success.value = '';
        isLoading.value = true;
        
        // Validate passwords match
        if (signupForm.password !== signupForm.confirmPassword) {
          error.value = 'Passwords do not match';
          isLoading.value = false;
          return;
        }
        
        // Create user in Firebase Authentication
        const userCredential = await createUserWithEmailAndPassword(
          auth, 
          signupForm.email, 
          signupForm.password
        );
        
        // Store additional user data in Firestore
        await setDoc(doc(db, 'users', userCredential.user.uid), {
          firstName: signupForm.firstName,
          lastName: signupForm.lastName,
          email: signupForm.email,
          phoneNumber: signupForm.phoneNumber,
          createdAt: new Date().toISOString(),
          authProvider: 'email'
        });
        
        success.value = 'Account created successfully! You can now login.';
        
        // Reset form fields
        Object.keys(signupForm).forEach(key => {
          signupForm[key] = '';
        });
        
        // Switch to login tab
        setTimeout(() => {
          activeTab.value = 'login';
        }, 1500);
        
      } catch (err) {
        error.value = translateFirebaseError(err.code) || 'Failed to create account. Please try again.';
      } finally {
        isLoading.value = false;
      }
    };
    
    // Google Authentication
    const signInWithGoogle = async () => {
      try {
        error.value = '';
        success.value = '';
        isGoogleLoading.value = true;
        
        const result = await signInWithPopup(auth, googleProvider);
        const user = result.user;
        
        // Check if user document exists in Firestore
        const userDoc = await getDoc(doc(db, 'users', user.uid));
        
        if (userDoc.exists()) {
          // Existing user - update login timestamp and redirect
          await updateDoc(doc(db, 'users', user.uid), {
            lastLogin: new Date().toISOString()
          });
          
          success.value = 'Login successful! Redirecting...';
          
          // Wait for auth store to update
          await authStore.init();
          
          // Redirect to main app after successful login
          setTimeout(() => {
            router.push('/findOutlet');
          }, 1000);
          
        } else {
          // New user - need additional information
          // Extract name from Google account if available
          let nameParts = ['', ''];
          if (user.displayName) {
            nameParts = user.displayName.split(' ');
          }
          
          googleAuthForm.uid = user.uid;
          googleAuthForm.email = user.email;
          googleAuthForm.firstName = nameParts[0] || '';
          googleAuthForm.lastName = nameParts.slice(1).join(' ') || '';
          googleAuthForm.phoneNumber = user.phoneNumber || '';
          
          // Switch to additional info form
          activeTab.value = 'additional-info';
        }
        
      } catch (err) {
        error.value = translateFirebaseError(err.code) || 'Google sign-in failed. Please try again.';
      } finally {
        isGoogleLoading.value = false;
      }
    };
    
    // Complete Google signup process with additional info
    const completeGoogleSignup = async () => {
      try {
        error.value = '';
        success.value = '';
        isLoading.value = true;
        
        // Store user data in Firestore
        await setDoc(doc(db, 'users', googleAuthForm.uid), {
          firstName: googleAuthForm.firstName,
          lastName: googleAuthForm.lastName,
          email: googleAuthForm.email,
          phoneNumber: googleAuthForm.phoneNumber,
          createdAt: new Date().toISOString(),
          authProvider: 'google'
        });
        
        success.value = 'Registration completed! Redirecting...';
        
        // Wait for auth store to update
        await authStore.init();
        
        // Redirect to main app after successful registration
        setTimeout(() => {
          router.push('/findOutlet');
        }, 1000);
        
      } catch (err) {
        error.value = 'Failed to complete registration. Please try again.';
        console.error(err);
      } finally {
        isLoading.value = false;
      }
    };
    
    // Password reset functionality
    const forgotPassword = async () => {
      try {
        if (!loginForm.email) {
          error.value = 'Please enter your email address';
          return;
        }
        
        isLoading.value = true;
        await sendPasswordResetEmail(auth, loginForm.email);
        success.value = 'Password reset email sent. Please check your inbox.';
        
      } catch (err) {
        error.value = translateFirebaseError(err.code) || 'Failed to send reset email. Please try again.';
      } finally {
        isLoading.value = false;
      }
    };
    
    // Translate Firebase error codes to user-friendly messages
    const translateFirebaseError = (errorCode) => {
      const errorMessages = {
        'auth/invalid-email': 'Invalid email address format',
        'auth/user-disabled': 'This account has been disabled',
        'auth/user-not-found': 'No account found with this email',
        'auth/wrong-password': 'Incorrect password',
        'auth/email-already-in-use': 'This email is already registered',
        'auth/weak-password': 'Password should be at least 6 characters',
        'auth/popup-closed-by-user': 'Authentication cancelled',
        'auth/cancelled-popup-request': 'Authentication cancelled',
        'auth/popup-blocked': 'Authentication popup was blocked by your browser'
      };
      
      return errorMessages[errorCode] || null;
    };
    
    return {
      activeTab,
      loginForm,
      signupForm,
      googleAuthForm,
      error,
      success,
      isLoading,
      isGoogleLoading,
      handleLogin,
      handleSignup,
      signInWithGoogle,
      completeGoogleSignup,
      forgotPassword
    };
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: var(--light);
}

.login-card {
  width: 100%;
  max-width: 500px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  overflow: hidden;
}

.login-header {
  background-color: var(--primary);
  color: white;
  padding: 2rem;
  text-align: center;
}

.login-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.login-logo img {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.login-logo h1 {
  font-size: 1.8rem;
  margin: 0;
}

.login-tagline {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0;
}

.login-tabs {
  display: flex;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.tab-btn {
  flex: 1;
  border: none;
  background-color: transparent;
  padding: 1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  color: var(--text-light);
}

.tab-btn.active {
  font-weight: bold;
  color: var(--primary);
  border-bottom: 2px solid var(--accent);
}

.tab-btn:hover:not(:disabled) {
  background-color: rgba(0,0,0,0.02);
}

.tab-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
  width: 100%;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text);
}

.form-group input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid rgba(0,0,0,0.2);
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(93, 64, 55, 0.2);
}

.form-group input:disabled {
  background-color: rgba(0,0,0,0.03);
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--dark);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.forgot-password {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-password:hover:not(.disabled) {
  text-decoration: underline;
}

.forgot-password.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.separator {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0;
}

.separator::before,
.separator::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.separator span {
  padding: 0 10px;
  color: var(--text-light);
  font-size: 0.9rem;
}

.btn-google {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid rgba(0,0,0,0.2);
  border-radius: 5px;
  padding: 0.8rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  position: relative;
}

.btn-google:hover:not(:disabled) {
  background-color: rgba(0,0,0,0.03);
}

.btn-google:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.google-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.error-message {
  background-color: #FFEBEE;
  color: #B71C1C;
  padding: 1rem;
  border-radius: 5px;
  margin: 1rem 2rem;
  font-size: 0.9rem;
}

.success-message {
  background-color: #E8F5E9;
  color: #1B5E20;
  padding: 1rem;
  border-radius: 5px;
  margin: 1rem 2rem;
  font-size: 0.9rem;
}

.info-text {
  margin-bottom: 1.5rem;
  color: var(--text-light);
}

/* Loading spinner */
.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.btn-google .spinner {
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--primary);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .login-card {
    max-width: 100%;
  }
  
  .login-form {
    padding: 1.5rem;
  }
}
</style>