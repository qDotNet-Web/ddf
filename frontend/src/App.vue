<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HomeView from './views/HomeView.vue';
import CreateLobbyView from './views/CreateLobbyView.vue';
</script>

<template>
  <header>
  </header>
  <HomeView />
  <router-view />
</template>

<!-- <style scoped>

</style> -->
