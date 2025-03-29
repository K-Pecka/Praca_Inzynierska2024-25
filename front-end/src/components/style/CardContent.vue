<script lang="ts" setup>
import { defineProps } from "vue";
import { DashboardBox } from "@/type/interface";

const props = defineProps<DashboardBox>();
</script>

<template>
  <v-card
    class="pa-4 rounded-lg"
    elevation="3"
    :style="{
      gridColumn: `span ${12}`,
      gridRow: `span ${2}`,
      order: props.set?.order,
    }"
  >
    <v-card-title class="text-h6 font-weight-medium d-flex align-center">
      <v-icon class="mr-2" color="primary">{{ props.icon }}</v-icon>
      {{ props.title }}
    </v-card-title>

    <v-card-text>
      <template v-if="Array.isArray(props.content)">
        <v-list v-if="props.content.length > 0">
          <v-list-item v-for="(item, index) in props.content" :key="index">
            <v-list-item-title>{{ item }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>

      <BudgetContent v-if="typeof props.content === 'object'" :content="props.content" />

      <template v-else>
        {{ props.content }}
      </template>
    </v-card-text>
  </v-card>
</template>

<script lang="ts" setup>
import BudgetContent from "@/components/BudgetContent.vue";
</script>
