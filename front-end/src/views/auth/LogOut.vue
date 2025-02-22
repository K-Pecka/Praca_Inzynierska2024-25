<script lang="ts" setup>
import { useUserStore } from "@/stores/auth/useAuthStore";
const { logout } = useUserStore();
logout();
</script>
<template></template>