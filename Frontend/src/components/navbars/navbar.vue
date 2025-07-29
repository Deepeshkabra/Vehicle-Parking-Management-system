<template>
  <nav class="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
    <div class="container-fluid">
      <!-- Brand -->
      <router-link class="navbar-brand" to="/">
        <i class="fas fa-car me-2"></i>
        ParkEase
      </router-link>

      <!-- Mobile toggle button -->
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarSupportedContent" 
        aria-controls="navbarSupportedContent" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar content -->
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- Left side navigation -->
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <!-- Admin Navigation -->
          <template v-if="authStore.user?.role === 'admin'">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/dashboard" :class="{ active: $route.path === '/admin/dashboard' }">
                <i class="fas fa-tachometer-alt me-1"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item dropdown">
              <a 
                class="nav-link dropdown-toggle" 
                href="#" 
                role="button" 
                data-bs-toggle="dropdown" 
                aria-expanded="false"
              >
                <i class="fas fa-building me-1"></i>
                Parking Lots
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/admin/parking-lots">
                    <i class="fas fa-list me-1"></i>
                    View All Lots
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/parking-lots/create">
                    <i class="fas fa-plus me-1"></i>
                    Add New Lot
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <router-link class="dropdown-item" to="/admin/spots">
                    <i class="fas fa-th me-1"></i>
                    Manage Spots
                  </router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/users" :class="{ active: $route.path === '/admin/users' }">
                <i class="fas fa-users me-1"></i>
                Users
              </router-link>
            </li>
          </template>

          <!-- User Navigation -->
          <template v-else-if="authStore.user?.role === 'user'">
            <li class="nav-item">
              <router-link class="nav-link" to="/dashboard" :class="{ active: $route.path === '/dashboard' }">
                <i class="fas fa-home me-1"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/parking-lots" :class="{ active: $route.path === '/parking-lots' }">
                <i class="fas fa-search me-1"></i>
                Find Parking
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/bookings" :class="{ active: $route.path === '/bookings' }">
                <i class="fas fa-calendar-check me-1"></i>
                My Bookings
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/history" :class="{ active: $route.path === '/history' }">
                <i class="fas fa-history me-1"></i>
                History
              </router-link>
            </li>
          </template>
        </ul>

        <!-- Right side navigation -->
        <div class="d-flex align-items-center">
          <!-- Search form (for users) -->
          <form 
            v-if="authStore.user?.role === 'user'" 
            class="d-flex me-3" 
            role="search"
            @submit.prevent="handleSearch"
          >
            <input 
              class="form-control me-2" 
              type="search" 
              placeholder="Search locations..." 
              aria-label="Search"
              v-model="searchQuery"
            >
            <button class="btn btn-outline-light" type="submit">
              <i class="fas fa-search"></i>
            </button>
          </form>

          <!-- User dropdown -->
          <div class="dropdown" v-if="authStore.isAuthenticated">
            <a 
              class="nav-link dropdown-toggle text-white d-flex align-items-center" 
              href="#" 
              role="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <i class="fas fa-user-circle me-2 fs-5"></i>
              {{ authStore.user?.username || 'User' }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <router-link class="dropdown-item" to="/profile">
                  <i class="fas fa-user me-2"></i>
                  Profile
                </router-link>
              </li>
              <li>
                <router-link class="dropdown-item" to="/settings">
                  <i class="fas fa-cog me-2"></i>
                  Settings
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a class="dropdown-item text-danger" href="#" @click="handleLogout">
                  <i class="fas fa-sign-out-alt me-2"></i>
                  Logout
                </a>
              </li>
            </ul>
          </div>

          <!-- Login/Register buttons (when not authenticated) -->
          <div v-else class="d-flex gap-2">
            <router-link to="/login" class="btn btn-outline-light btn-sm">
              Login
            </router-link>
            <router-link to="/register" class="btn btn-light btn-sm">
              Register
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/parking-lots',
      query: { search: searchQuery.value.trim() }
    })
  }
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<style scoped>
.navbar-brand {
  font-weight: 600;
  font-size: 1.5rem;
}

.nav-link.active {
  font-weight: 600;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.375rem;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

/* Custom mobile styles */
@media (max-width: 991px) {
  .navbar-nav {
    margin-top: 1rem;
  }
  
  .navbar-nav .nav-link {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .d-flex.gap-2 {
    margin-top: 1rem;
    justify-content: center;
  }
}
</style>
