<template>
    <div v-if="visible" class="popup-overlay">
      <div class="popup-box">
        <h3>{{ title }}</h3>
        <p>{{ message }}</p>
        <button @click="closePopup" class="popup-button">OK</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      visible: {
        type: Boolean,
        required: true,
      },
      title: {
        type: String,
        default: "Message",
      },
      message: {
        type: String,
        required: true,
      },
    },
    methods: {
      closePopup() {
        this.$emit("close");
      },
    },
  };
  </script>
  
  <style scoped>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  }
  
  .popup-box {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    width: 100%;
  }
  
  .popup-box h3 {
    margin-bottom: 1rem;
    font-size: 1.5rem;
    color: var(--primary);
  }
  
  .popup-box p {
    margin-bottom: 1.5rem;
    font-size: 1rem;
    color: var(--text);
  }
  
  .popup-button {
    padding: 0.75rem 1.5rem;
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.3s;
  }
  
  .popup-button:hover {
    background-color: var(--secondary);
  }
  </style>