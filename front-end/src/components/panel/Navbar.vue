<script lang="ts" setup>
import {useRouter} from "vue-router";
import {computed, watch,ref} from "vue";
import {usePagePanelStore} from "@/stores"
import { useTripStore } from "@/stores";
import { Role } from "@/types/enum";
import { useRoleStore } from "@/stores/auth/useRoleStore";
import {SideNavItem} from "@/types"
usePagePanelStore().initialize();
const {getSideNavItems} = usePagePanelStore();
const router = useRouter();
const {getRole} = useRoleStore()
const props = defineProps({
  modelValue: Boolean,
})
const { trip } = useTripStore();
const {getTripDetails} = trip;
const { trip: tripDetails } = getTripDetails();

const side_nav_items = ref<SideNavItem[]>([]);

watch(tripDetails, (newVal) => {
  if (newVal?.creator?.type !== undefined) {
    const creatorType = Number(newVal.creator.type);
    const tripType = !isNaN(creatorType) && (creatorType === 2 || getRole() === Role.GUIDE)
      ? Role.GUIDE
      : Role.TOURIST;

    side_nav_items.value = getSideNavItems(tripType);
  }
}, { immediate: true });

const emit = defineEmits(['update:modelValue'])
const drawer = computed({
  get: () => props.modelValue,
  set: val => emit('update:modelValue', val)
})
</script>

<template>
  <v-navigation-drawer
      style="z-index: 1006;"
      class="navbar-border font-weight-bold"
      v-model="drawer"
  >
    <!-- Navigation Drawer -->
    <v-list>
      <template v-for="item in side_nav_items">

        <!-- Pages with children -->
        <v-list-group
            v-if="item.children"
            prepend-icon="mdi-chevron-down"
        >
          <template #activator="{ props }">
            <v-list-item
                v-bind="props"
                :title="item.title"
                :prepend-icon="item.icon"
                slim
                class="pl-3"
            />
          </template>

          <v-list-item
              v-for="subItem in item.children"
              :key="subItem.title"
              :title="subItem.title"
              :active="router.currentRoute.value.name === subItem.page.name"
              @click="router.push(subItem.page)"
              slim
              class="pl-6"
          />
        </v-list-group>
        <!-- Pages without children -->
        <v-list-item
            v-else
            :title="item.title"
            :prepend-icon="item.icon"
            :active="router.currentRoute.value.name === item?.page?.name"
            @click="router.push(item.page || '')"
            slim
            class="pl-3"
        />
      </template>
      <v-divider/>
    </v-list>

    <!-- Return button -->
    <v-list-item
        title="Powrót"
        link
        prepend-icon="mdi-arrow-left"
        slim
        class="pl-3"
        @click="router.push({ name: 'ChooseTrip' })"
    />
  </v-navigation-drawer>
</template>

<style scoped lang="scss">
.navbar-border {
    border-right: 2px solid blue !important;
}
</style>

