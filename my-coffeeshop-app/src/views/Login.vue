<template>
    <div class="login-container">
      <div class="login-card">
        <div class="brand">
          <h1>Brew Heaven</h1>
          <p class="tagline">Crafting Perfect Moments</p>
        </div>
        
        <div class="tabs">
          <button 
            :class="['tab-btn', { active: activeTab === 'login' }]" 
            @click="activeTab = 'login'"
          >
            Login
          </button>
          <button 
            :class="['tab-btn', { active: activeTab === 'register' }]" 
            @click="activeTab = 'register'"
          >
            Create Account
          </button>
        </div>
        
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input 
              type="email" 
              id="email" 
              v-model="loginForm.email" 
              placeholder="your@email.com" 
              required
            >
          </div>
          
          <div class="form-group">
            <label for="password">Password</label>
            <input 
              type="password" 
              id="password" 
              v-model="loginForm.password" 
              placeholder="Enter your password" 
              required
            >
          </div>
          
          <button type="submit" class="submit-btn">Log In</button>
          <a href="#" class="forgot-password" @click.prevent="handleForgotPassword">Forgot Password?</a>
        </form>
        
        <form v-else @submit.prevent="handleRegister" class="login-form">
          <div class="form-group">
            <label for="reg-name">Full Name</label>
            <input 
              type="text" 
              id="reg-name" 
              v-model="registerForm.name" 
              placeholder="Your name" 
              required
            >
          </div>

          <div class="form-group">
            <label for="reg-name">Phone Number</label>
            <input 
              type="number" 
              id="reg-phone" 
              v-model="registerForm.phone" 
              placeholder="91239843" 
              required
            >
          </div>
          
          <div class="form-group">
            <label for="reg-email">Email</label>
            <input 
              type="email" 
              id="reg-email" 
              v-model="registerForm.email" 
              placeholder="your@email.com" 
              required
            >
          </div>
          
          <div class="form-group">
            <label for="reg-password">Password</label>
            <input 
              type="password" 
              id="reg-password" 
              v-model="registerForm.password" 
              placeholder="Create a password" 
              required
            >
          </div>
          
          <button type="submit" class="submit-btn">Create Account</button>
        </form>
        
        <div class="divider">
          <span>or</span>
        </div>
        
        <button @click="signInWithGoogle" class="google-btn">
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google logo">
          Continue with Google
        </button>
        
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { ref, reactive } from 'vue'
  import { 
    getAuth, 
    signInWithEmailAndPassword, 
    createUserWithEmailAndPassword, 
    GoogleAuthProvider, 
    signInWithPopup,
    sendPasswordResetEmail
  } from 'firebase/auth'
  import { useRouter } from 'vue-router';

  
  export default {
    name: 'LoginComponent',
    setup() {
      const router = useRouter();
      const activeTab = ref('login')
      const errorMessage = ref('')
      
      const loginForm = reactive({
        email: '',  
        password: ''
      })
      
      const registerForm = reactive({
        name: '',
        phone: '',
        email: '',
        password: ''
      })
      
      const auth = getAuth()
      
      const handleLogin = async () => {
        try {
          errorMessage.value = ''
          await signInWithEmailAndPassword(auth, loginForm.email, loginForm.password)
          // Redirect or handle successful login
          
          // console.log('Logged in successfully')
          alert('You have been logged in successfully!')
          localStorage.setItem("selectedOutletId",'something' )
          
          console.log(router)
          router.push(`/findOutlet`)
        } catch (error) {
          errorMessage.value = getErrorMessage(error.code)
        }
      }
      
      //new handleregister funtion 
      const handleRegister = async () => {
      try {
        errorMessage.value = '';

        // Step 1: We create Firebase Auth account
        const userCredential = await createUserWithEmailAndPassword(
          auth,
          registerForm.email,
          registerForm.password
        );

        // Step 2: Send user data to Flask `/register` endpoint (login.py)
        const response = await axios.post('http://localhost:5019/register', {
          email: registerForm.email,
          password: registerForm.password,
          username: registerForm.name,
          phoneNum: registerForm.phone
        });

        if (response.status === 201) {
          console.log('Account registered and profile created!');
          alert('Registration successful!');
          router.push('/login');  // Or wherever you want to redirect
        } else {
          errorMessage.value = response.data.error || 'Something went wrong.';
        }

      } catch (error) {
        if (error.response) {
          // Error returned by Flask backend
          errorMessage.value = error.response.data.details || 'Backend registration error.';
        } else {
          // Firebase error
          errorMessage.value = getErrorMessage(error.code);
        }
      }
    };

      
      const signInWithGoogle = async () => {
        try {
          errorMessage.value = ''
          const provider = new GoogleAuthProvider()
          await signInWithPopup(auth, provider)
          // Redirect or handle successful login
          console.log('Logged in with Google successfully')

          alert('You have been logged in successfully!')
          
          console.log(router)
          router.push(`/findOutlet`)
        } catch (error) {
          errorMessage.value = 'Google sign-in failed. Please try again.'
        }
      }
      
      const handleForgotPassword = async () => {
        if (!loginForm.email) {
          errorMessage.value = 'Please enter your email address'
          return
        }
        
        try {
          await sendPasswordResetEmail(auth, loginForm.email)
          errorMessage.value = 'Password reset email sent! Check your inbox.'
        } catch (error) {
          errorMessage.value = 'Failed to send reset email. Please try again.'
        }
      }
      
      const getErrorMessage = (errorCode) => {
        switch (errorCode) {
          case 'auth/invalid-email':
            return 'Invalid email address.'
          case 'auth/user-disabled':
            return 'This account has been disabled.'
          case 'auth/user-not-found':
            return 'No account found with this email.'
          case 'auth/wrong-password':
            return 'Incorrect password.'
          case 'auth/email-already-in-use':
            return 'This email is already registered.'
          case 'auth/weak-password':
            return 'Password should be at least 6 characters.'
          default:
            return 'An error occurred. Please try again.'
        }
      }
      
      return {
        activeTab,
        loginForm,
        registerForm,
        errorMessage,
        handleLogin,
        handleRegister,
        signInWithGoogle,
        handleForgotPassword
      }
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: var(--light);
    background-image: linear-gradient(rgba(239, 235, 233, 0.8), rgba(239, 235, 233, 0.8)), 
                      url('path-to-your-coffee-background.jpg');
    background-size: cover;
    background-position: center;
  }
  
  .login-card {
    width: 100%;
    max-width: 450px;
    background-color: white;
    border-radius: 10px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }
  
  .brand {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .brand h1 {
    color: var(--primary);
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  
  .tagline {
    color: var(--text-light);
    font-size: 1rem;
  }
  
  .tabs {
    display: flex;
    border-bottom: 1px solid #eee;
    margin-bottom: 1.5rem;
  }
  
  .tab-btn {
    flex: 1;
    background: none;
    border: none;
    padding: 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-light);
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .tab-btn.active {
    color: var(--primary);
    border-bottom: 2px solid var(--primary);
  }
  
  .login-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  label {
    font-weight: 600;
    color: var(--text);
    font-size: 0.9rem;
  }
  
  input {
    padding: 0.75rem 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    transition: border-color 0.3s;
  }
  
  input:focus {
    outline: none;
    border-color: var(--primary);
  }
  
  .submit-btn {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 0.5rem;
  }
  
  .submit-btn:hover {
    background-color: var(--dark);
  }
  
  .forgot-password {
    text-align: center;
    color: var(--primary);
    text-decoration: none;
    font-size: 0.9rem;
    margin-top: 1rem;
    display: block;
  }
  
  .divider {
    position: relative;
    text-align: center;
    margin: 1.5rem 0;
  }
  
  .divider::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background-color: #eee;
  }
  
  .divider span {
    position: relative;
    background-color: white;
    padding: 0 1rem;
    color: var(--text-light);
    font-size: 0.9rem;
  }
  
  .google-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    width: 100%;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 0.75rem;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .google-btn:hover {
    background-color: #f5f5f5;
  }
  
  .google-btn img {
    width: 18px;
    height: 18px;
  }
  
  .error-message {
    color: #d32f2f;
    font-size: 0.9rem;
    margin-top: 1rem;
    text-align: center;
  }
  </style>