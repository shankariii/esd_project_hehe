<template>
    <div class="error-page">
      <div class="error-container">
        <div class="coffee-cup">
          <img src="../assets/drink_logo.png" alt="404 Error - Coffee Cup" />
        </div>
        <h1>Oops! Page Not Found</h1>
        <p>Looks like this brew went missing...</p>
        <p class="error-message">The page you're looking for has been spilled or doesn't exist.</p>
        <router-link to="/" class="home-button">
          Back to Brew Haven
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Error404Page'
  }
  </script>
  
  <style scoped>
  .error-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--light);
    padding: 2rem;
  }
  
  .error-container {
    max-width: 600px;
    text-align: center;
    background-color: white;
    padding: 3rem 2rem;
    border-radius: 10px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  }
  
  .coffee-cup {
    width: 250px;
    height: 250px;
    margin: 0 auto 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .coffee-cup img {
    max-width: 100%;
    height: auto;
  }
  
  h1 {
    color: var(--primary);
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  p {
    color: var(--text-light);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
  }
  
  .error-message {
    margin-bottom: 2rem;
  }
  
  .home-button {
    display: inline-block;
    background-color: var(--primary);
    color: white;
    padding: 1rem 2rem;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
  }
  
  .home-button:hover {
    background-color: var(--dark);
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  }
  
  @media (max-width: 768px) {
    .coffee-cup {
      width: 180px;
      height: 180px;
    }
    
    h1 {
      font-size: 2rem;
    }
    
    p {
      font-size: 1rem;
    }
  }
  </style>