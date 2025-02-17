<script lang="ts" setup>
import { useUserStore } from "@/stores/userStore";
const { logout } = useUserStore();
logout();
</script>
<template></template>