<template>
  <nav class="navbar">
    <div class="navbar__container">
      <div class="navbar__logo">
        <slot name="logo">
          <h1>Logo</h1>
        </slot>
      </div>
      <ul class="navbar__links">
        <li v-for="(link, index) in links" :key="index" class="navbar__item">
          <a
            :href="link.href"
            class="navbar__link"
            :class="{ active: link.active }"
            :style="link.style"
            aria-current="page"
          >
            {{ link.label }}
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script lang="ts" setup>
interface Link {
  label: string;
  href: string;
  style?: Record<string, string>;
  active?: boolean;
}

defineProps<{ links: Link[] }>();
</script>

<style scoped lang="scss">
$primary-color: var(--primary-color);
$text-color: var(--text-color);
$background-color: var(--background-color);
$border-radius: var(--border-radius);
$font-family: var(--font-family);
@use "@/assets/style" as *;
.navbar {
  @include section-width;
  margin: 1rem auto;
  padding: 1rem;
  height: 6rem;
  background-color: $background-color;
  border: 2px solid $primary-color;
  border-radius: $border-radius;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: $font-family;
  transition: all 0.3s ease-in-out;

  .navbar__container {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .navbar__logo {
    padding: 1rem;
    font-size: 1.5rem;
    color: $primary-color;
  }

  .navbar__links {
    display: flex;
    list-style: none;
    gap: 1rem;
    padding: 0.5rem;
    margin: 0;
  }

  .navbar__item {
    list-style: none;
  }

  .navbar__link {
    padding: 10px;
    text-decoration: none;
    color: $text-color;
    font-weight: bold;
    transition: color 0.3s ease, background-color 0.3s ease;

    &.active {
      color: #fff;
      padding: calc(1rem + 4px);
      background-color: $primary-color;
      border-radius: calc($border-radius - 9px);
    }
  }
}
</style>
