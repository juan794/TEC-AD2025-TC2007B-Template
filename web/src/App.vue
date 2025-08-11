<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div class="container mx-auto">
    <NavBar />
    <RouterView />
  </div>
</template>