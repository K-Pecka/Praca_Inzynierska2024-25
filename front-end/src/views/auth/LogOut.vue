<script lang="ts" setup>
import { useAuthStore,usePageHomeStore } from "@/stores";
const { logout } = useAuthStore();
const { setStateisLogged } = usePageHomeStore();
logout();
setStateisLogged(false);
</script>
<template></template>