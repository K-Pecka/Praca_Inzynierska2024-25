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

<script setup lang="ts"></script>

<style scoped>
.btn {
  display: flex;
  padding: 1rem;
  border: none;
  background-color: var(--secondary-color);
  color: var(--color-text);
  width: 80%;
  border-radius: 4px;
  margin: 0.25rem auto;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: var(--primary-color);
}

.btn-icon {
  flex: 1;
}

.btn-text {
  flex: 9;
  font-weight: bold;
}
</style>
