<script lang="ts" setup>
import { useAuthStore } from "@/stores";
const { logout } = useAuthStore();
logout();
</script>
<template></template>