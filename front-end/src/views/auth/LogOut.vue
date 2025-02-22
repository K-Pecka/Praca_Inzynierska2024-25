<script lang="ts" setup>
import { useAuthStore } from "@/stores/auth/useAuthStore";
const { logout } = useAuthStore();
logout();
</script>
<template></template>