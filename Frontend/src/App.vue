<script setup>
import { computed } from 'vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Navbar from './components/navbars/navbar.vue'
import Dashboard from './views/admin/Dashboard.vue'

const route = useRoute()
const authStore = useAuthStore()

// Initialize auth state
authStore.initializeAuth()
</script>

<template>
  <div id="app">
    <Navbar />
    <!-- Main Content -->
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
#app {
  min-height: fit-content;
}

.navbar-brand {
  font-weight: bold;
}

.dropdown-toggle::after {
  margin-left: 0.5em;
}
</style>
