<template>
    <button class="btn">
     
      <span class="btn-icon">
        <slot name="icon"></slot>
      </span>

      <span class="btn-text">
        <slot name="text"></slot>
      </span>
    </button>
  </template>
  
  <script setup lang="ts">
  </script>
  
  <style scoped>
  .btn {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    border: none;
    background-color: #007bff;
    width: 100%;
    border-radius: 4px;
    margin:0.25rem auto;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  .btn-icon {
    width: 1.25rem;
    height: 1.25rem;
  }
  
  .btn-text {
    font-weight: bold;
  }
  </style>
  