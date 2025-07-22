<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
/* Global styles */
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
}

/* Override Vue default styles for full layout */
body, html {
  margin: 0;
  padding: 0;
}
</style>
