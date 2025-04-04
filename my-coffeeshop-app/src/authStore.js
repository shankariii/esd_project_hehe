// src/stores/authStore.js
import { defineStore } from 'pinia';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, getDoc } from 'firebase/firestore';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    userProfile: null,
    isLoading: true,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.user,
    userFullName: (state) => {
      if (!state.userProfile) return '';
      return `${state.userProfile.firstName} ${state.userProfile.lastName}`;
    }
  },
  
  actions: {
    async init() {
      const auth = getAuth();
      
      return new Promise((resolve) => {
        // This listener persists across page refreshes
        onAuthStateChanged(auth, async (user) => {
          this.isLoading = true;
          this.error = null;
          
          if (user) {
            // User is signed in
            this.user = {
              uid: user.uid,
              email: user.email,
              displayName: user.displayName,
              photoURL: user.photoURL
            };
            
            // Get additional user data from Firestore
            try {
              const db = getFirestore();
              const userDoc = await getDoc(doc(db, 'users', user.uid));
              
              if (userDoc.exists()) {
                this.userProfile = userDoc.data();
              }
            } catch (err) {
              console.error('Error fetching user profile:', err);
              this.error = 'Failed to load user profile';
            }
          } else {
            // User is signed out
            this.user = null;
            this.userProfile = null;
          }
          
          this.isLoading = false;
          resolve();
        });
      });
    },
    
    async logout() {
      const auth = getAuth();
      try {
        await auth.signOut();
      } catch (err) {
        console.error('Error signing out:', err);
        this.error = 'Failed to sign out';
      }
    }
  }
});