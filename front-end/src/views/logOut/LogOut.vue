<script lang="ts" setup>
import { useUserStore } from "@/stores/userStore";
import { useRouter } from 'vue-router';
const router = useRouter();
const { logout } = useUserStore();
logout();
router.push('/');
</script>
<template></template>