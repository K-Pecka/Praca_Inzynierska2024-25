<script lang="ts" setup>
import { ref, defineProps, defineEmits } from "vue";
import { SideNavItem } from "@/type/interface";


const props = defineProps<{
  items: SideNavItem[];
  mobile?: boolean;
}>();

const emit = defineEmits(["close"]);

const openIndex = ref<number | null>(null);

function toggleSection(index: number) {
  openIndex.value = openIndex.value === index ? null : index;
}

const arrowIcon = "/picture/sideNav/arrow.svg";

</script>

<template>
  <nav class="side-nav" :class="{ mobile }">
    <button v-if="mobile" class="close-btn" @click="emit('close')">
      <v-icon size="42">mdi-close</v-icon>
    </button>

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
          <v-icon v-if="item.icon" class="side-nav__icon">{{
              openIndex === index && item.iconActive
                  ? item.iconActive
                  : item.icon}}</v-icon>
          <router-link
              v-if="item.route"
              :to="item.route"
              class="side-nav__item-link"
              @click="mobile ? emit('close') : null"
          >
            {{ item.label }}
          </router-link>

          <span v-else>{{ item.label }}</span>

          <v-icon
              v-if="item.children"
              class="side-nav__arrow-icon"
              :class="{ open: openIndex === index }"
          >mdi-chevron-right</v-icon>
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
                @click="mobile ? emit('close') : null"
            >
              {{ sub.label }}
            </router-link>
          </li>
        </ul>
      </li>
    </ul>
  </nav>
</template>

<style lang="scss" scoped>
.side-nav {
  height: 100%;
  left: 0;
  background: rgba(#F5F4FC,0.75);
  border-right: 2px solid rgb(var(--v-theme-primary));
  padding: 1rem;
  overflow-y: auto;
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


@media (max-width: 1000px) {
  .side-nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.9);
    z-index: 2000;
    padding-top: 0;
    overflow-y: auto;
    display: flex;

    align-items: center;
    justify-content: center;
  }

  .side-nav__list {
    width: auto;
    max-width: 450px;
    text-align: left;
  }

  .side-nav__item {
    margin-bottom: 1.5rem;
    width: 100%;
  }

  .side-nav__item-header {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 0.5rem;
    cursor: pointer;
    font-weight: 600;
    color: #ffffff;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.2);
  }

  .side-nav__icon {
    width: 24px;
    height: 24px;
    filter: brightness(0) invert(1);
  }

  .side-nav__arrow-icon {
    width: 24px;
    height: 24px;
    margin-left: 0.5rem;
    filter: brightness(0) invert(1);
    transition: transform 0.3s ease;

    &.open {
      transform: rotate(90deg);
    }
  }

  .side-nav__sub-list {
    margin-top: 1rem;
    margin-left: 0;
    list-style: none;
    padding-left: 1.5rem;
  }

  .side-nav__sub-item {
    margin-bottom: 1rem;
  }

  .side-nav__sub-link,
  .side-nav__item-link {
    text-decoration: none;
    color: rgba(255, 255, 255, 0.85);
    font-size: 1.1rem;

    &:hover {
      color: rgb(var(--v-theme-primary));
    }
  }

  .close-btn {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    color: #ffffff;
    font-size: 2rem;
    cursor: pointer;
    z-index: 2001;
  }
}

</style>
