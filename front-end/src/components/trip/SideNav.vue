<script lang="ts" setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { SideNavItem } from "@/type/interface";


const props = defineProps<{
  items: SideNavItem[];
}>();

const openIndex = ref<number | null>(null);

function toggleSection(index: number) {
  openIndex.value = openIndex.value === index ? null : index;
}

const arrowIcon = "/picture/sideNav/arrow.svg";

</script>

<template>
  <div class="side-nav">
    <ul class="side-nav__list">
      <li
          v-for="(item, index) in items"
          :key="item.label"
          class="side-nav__item"
      >
        <div
            class="side-nav__item-header"
            :class="{ open: openIndex === index }"
            @click="item.children ? toggleSection(index) : null"
        >
          <img
              v-if="item.icon"
              :src="openIndex === index && item.iconActive
                      ? item.iconActive
                      : item.icon"
              class="side-nav__icon"
              alt=""
          />

          <router-link
              v-if="item.route"
              :to="item.route"
              class="side-nav__item-link"
          >
            {{ item.label }}
          </router-link>

          <span v-else>{{ item.label }}</span>

          <img
              v-if="item.children"
              :src="arrowIcon"
              class="side-nav__arrow-icon"
              :class="{ open: openIndex === index }"
              alt="arrow"
          />
        </div>


        <ul
            v-if="item.children"
            class="side-nav__sub-list"
            v-show="openIndex === index"
        >
          <li
              v-for="sub in item.children"
              :key="sub.label"
              class="side-nav__sub-item"
          >
            <router-link
                v-if="sub.route"
                :to="sub.route"
                class="side-nav__sub-link"
            >
              {{ sub.label }}
            </router-link>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.side-nav {
  left: 0;
  background: rgba(#F5F4FC,0.75);
  border-right: 2px solid rgb(var(--v-theme-primary));
  padding: 1rem;
}

.side-nav__list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side-nav__item {
  margin-bottom: 1.8rem;
}

.side-nav__item-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  color: rgb(var(--v-theme-text));
}

.side-nav__icon {
  width: 24px;
  height: 24px;
}

.side-nav__arrow-icon {
  width: 24px;
  height: 24px;
  margin-left: 0.5rem;
  transition: transform 0.3s ease;

  &.open {
    transform: rotate(90deg);
  }
}

.side-nav__sub-list {
  margin: 0.5rem 0 0.5rem 2rem;
  list-style: none;
  padding: 0.5rem;
}

.side-nav__sub-item {
  margin-bottom: 0.5rem;
}

.side-nav__sub-link,
.side-nav__item-link {
  text-decoration: none;
  color: rgb(var(--v-theme-text));
  &:hover {
    color: rgb(var(--v-theme-primary));
  }
}

</style>
