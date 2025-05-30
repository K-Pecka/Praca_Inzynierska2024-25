<script lang="ts" setup>
import { useAuthStore } from "@/stores";
import router from "@/router";
const { logout,userData } = useAuthStore();
const {getUser} = userData
if(getUser()){
    logout();
}
else
{
   router.push({ name: "landing" });
}
</script>
<template></template>