<script lang="ts" setup>
import {ref, onMounted} from "vue";
import {SideNavItem} from "@/type/interface";
import {usePermissionStore, useAuthStore} from "@/stores";
import {useRoute} from "vue-router";
import {usePagePanelStore, useUtilStore} from "@/stores";
import {Role} from "@/type/enum";

const {getSideNavItems} = usePagePanelStore();
const route = useRoute();
usePagePanelStore().initialize(route.name as string);
const items: SideNavItem[] = getSideNavItems(
    useUtilStore().getTripId().value as string
);
const {checkPermission} = useAuthStore();
const {goTo} = usePermissionStore();

const props = defineProps<{
  mobile?: boolean;
}>();

const emit = defineEmits(["close"]);
const openIndex = ref<number | null>(null);
const accessMap = ref<Record<string, boolean>>({});

const checkAccess = async () => {
  const permissions = await Promise.all(
      items.flatMap((item) =>
          [item, ...(item.children ?? [])].map(async (subItem) => ({
            name: subItem.name,
            hasAccess: true//await checkPermission(subItem.name, "nav"),
          }))
      )
  );

  accessMap.value = {
    "": true,
    ...Object.fromEntries(permissions.map((p) => [p.name, p.hasAccess])),
  };
};

const linkTo = (item: SideNavItem) => {
  return item.name && item.route && accessMap.value[item.name] ? item.route : goTo();
}


onMounted(checkAccess);

function toggleSection(index: number) {
  openIndex.value = openIndex.value === index ? null : index;
}

function closeSideNavWithDelay() {
  setTimeout(() => emit('close'), 50);
}
</script>

<template>
  <nav class="side-nav" :class="{ mobile }">


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
          <v-icon v-if="item.icon" class="side-nav__icon">
            {{
              openIndex === index && item.iconActive
                  ? item.iconActive
                  : item.icon
            }}
          </v-icon>

          <router-link
              v-if="item.route"
              :to="linkTo(item)"
              class="side-nav__item-link"
              @click="props.mobile ? closeSideNavWithDelay() : null"
              :class="{ 'no-permission': !accessMap[item.name || ''] }"
          >
            {{ item.label }}
          </router-link>

          <span v-else>{{ item.label }}</span>

          <v-icon
              v-if="item.children"
              class="side-nav__arrow-icon"
              :class="{ open: openIndex === index }"
          >
            mdi-chevron-right
          </v-icon>
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
                :to="linkTo(sub)"
                class="side-nav__sub-link"
                :class="{ 'no-permission': !accessMap[sub.name || ''] }"
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
.no-permission {
  opacity: 0.5;
}

.no-permission::after {
  content: "⭐";
}

.side-nav {
  height: 100%;
  left: 0;
  background-color: rgba(var(--v-theme-background));
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

@media (min-width: 1980px) {
  .side-nav__item-header,
  .side-nav__sub-link,
  .side-nav__item-link {
    font-size: 1.5rem;
  }
}

@media (min-width: 959px) and (max-width: 1200px) {
  .side-nav__item-header,
  .side-nav__sub-link,
  .side-nav__item-link {
    font-size: 1rem;
  }
}
</style>
