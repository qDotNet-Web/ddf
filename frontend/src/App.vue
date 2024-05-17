<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
</script>

<template>
  <header>
  </header>
  <Toast position="top-right" />
  <ConfirmDialog />
  <router-view />
</template>

<!-- <style scoped>

</style> -->
