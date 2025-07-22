<template>
  <div class="dashboard-page">
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link to="/" class="navbar-brand">
          <i class="bi bi-car-front me-2"></i>
          ParkingManager
        </router-link>
        
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">
                <i class="bi bi-speedometer2 me-1"></i>
                Dashboard
              </router-link>
            </li>
            <li v-if="authStore.isAdmin" class="nav-item">
              <router-link to="/admin" class="nav-link">
                <i class="bi bi-gear me-1"></i>
                Admin Panel
              </router-link>
            </li>
            <li v-if="authStore.isUser" class="nav-item">
              <router-link to="/bookings" class="nav-link">
                <i class="bi bi-calendar-check me-1"></i>
                My Bookings
              </router-link>
            </li>
          </ul>
          
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a 
                class="nav-link dropdown-toggle" 
                href="#" 
                id="navbarDropdown" 
                role="button" 
                data-bs-toggle="dropdown"
              >
                <i class="bi bi-person-circle me-1"></i>
                {{ authStore.userName }}
              </a>
              <ul class="dropdown-menu">
                <li>
                  <span class="dropdown-item-text">
                    <small class="text-muted">{{ authStore.userRole?.toUpperCase() }}</small>
                  </span>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="handleProfile">
                    <i class="bi bi-person me-2"></i>
                    Profile
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="handleSettings">
                    <i class="bi bi-gear me-2"></i>
                    Settings
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">
                    <i class="bi bi-box-arrow-right me-2"></i>
                    Logout
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container-fluid py-4">
      <!-- Welcome Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="h3 mb-0">
                Welcome back, {{ authStore.userName }}! 
                <span class="badge bg-primary ms-2">{{ authStore.userRole?.toUpperCase() }}</span>
              </h1>
              <p class="text-muted mb-0">
                Last login: {{ formatDate(authStore.user?.last_login) }}
              </p>
            </div>
            <div class="d-flex gap-2">
              <button 
                class="btn btn-outline-primary"
                @click="refreshData"
                :disabled="isLoading"
              >
                <i class="bi bi-arrow-clockwise me-1"></i>
                Refresh
              </button>
              <router-link 
                :to="authStore.isAdmin ? '/admin' : '/bookings'" 
                class="btn btn-primary"
              >
                <i class="bi bi-plus-circle me-1"></i>
                {{ authStore.isAdmin ? 'Admin Panel' : 'New Booking' }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Admin Dashboard -->
      <div v-if="authStore.isAdmin" class="admin-dashboard">
        <div class="row mb-4">
          <div class="col-md-3 mb-3" v-for="stat in adminStats" :key="stat.id">
            <div class="card text-center h-100">
              <div class="card-body">
                <div class="stat-icon mb-2">
                  <i :class="stat.icon" class="display-4" :style="{ color: stat.color }"></i>
                </div>
                <h3 class="fw-bold mb-1">{{ stat.value }}</h3>
                <p class="text-muted mb-0">{{ stat.label }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-lg-8 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-graph-up me-2"></i>
                  System Overview
                </h5>
              </div>
              <div class="card-body">
                <div class="alert alert-info">
                  <i class="bi bi-info-circle me-2"></i>
                  <strong>Admin Features:</strong> Full parking lot management, user oversight, and system analytics.
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <h6>Quick Actions</h6>
                    <div class="list-group list-group-flush">
                      <a href="#" class="list-group-item list-group-item-action">
                        <i class="bi bi-building me-2"></i>
                        Manage Parking Lots
                      </a>
                      <a href="#" class="list-group-item list-group-item-action">
                        <i class="bi bi-people me-2"></i>
                        View All Users
                      </a>
                      <a href="#" class="list-group-item list-group-item-action">
                        <i class="bi bi-file-text me-2"></i>
                        Generate Reports
                      </a>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <h6>System Status</h6>
                    <div class="mb-2">
                      <small class="text-muted">Server Status</small>
                      <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: 100%"></div>
                      </div>
                      <small class="text-success">Online</small>
                    </div>
                    <div class="mb-2">
                      <small class="text-muted">Database</small>
                      <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: 95%"></div>
                      </div>
                      <small class="text-success">Healthy</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-4 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-activity me-2"></i>
                  Recent Activity
                </h5>
              </div>
              <div class="card-body">
                <div class="timeline">
                  <div class="timeline-item mb-3" v-for="activity in recentActivity" :key="activity.id">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i :class="activity.icon" class="text-primary"></i>
                      </div>
                      <div class="flex-grow-1 ms-2">
                        <small class="text-muted">{{ activity.time }}</small>
                        <p class="mb-0">{{ activity.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Dashboard -->
      <div v-else class="user-dashboard">
        <div class="row mb-4">
          <div class="col-md-4 mb-3" v-for="stat in userStats" :key="stat.id">
            <div class="card text-center h-100">
              <div class="card-body">
                <div class="stat-icon mb-2">
                  <i :class="stat.icon" class="display-4" :style="{ color: stat.color }"></i>
                </div>
                <h3 class="fw-bold mb-1">{{ stat.value }}</h3>
                <p class="text-muted mb-0">{{ stat.label }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-lg-8 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-calendar-check me-2"></i>
                  My Parking Activity
                </h5>
              </div>
              <div class="card-body">
                <div class="alert alert-success">
                  <i class="bi bi-check-circle me-2"></i>
                  <strong>Welcome!</strong> Your parking account is active and ready to use.
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <h6>Quick Actions</h6>
                    <div class="d-grid gap-2">
                      <button class="btn btn-primary">
                        <i class="bi bi-plus-circle me-2"></i>
                        Book Parking Spot
                      </button>
                      <button class="btn btn-outline-primary">
                        <i class="bi bi-search me-2"></i>
                        Find Available Lots
                      </button>
                      <button class="btn btn-outline-secondary">
                        <i class="bi bi-clock-history me-2"></i>
                        View History
                      </button>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <h6>Account Status</h6>
                    <div class="mb-2">
                      <small class="text-muted">Account Status</small>
                      <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-success" style="width: 100%"></div>
                      </div>
                      <small class="text-success">Active</small>
                    </div>
                    <div class="mb-2">
                      <small class="text-muted">Available Bookings</small>
                      <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-info" style="width: 80%"></div>
                      </div>
                      <small class="text-info">Unlimited</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-4 mb-4">
            <div class="card h-100">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-info-circle me-2"></i>
                  Getting Started
                </h5>
              </div>
              <div class="card-body">
                <div class="list-group list-group-flush">
                  <div class="list-group-item border-0 px-0">
                    <i class="bi bi-1-circle text-primary me-2"></i>
                    Browse available parking lots
                  </div>
                  <div class="list-group-item border-0 px-0">
                    <i class="bi bi-2-circle text-primary me-2"></i>
                    Book your preferred spot
                  </div>
                  <div class="list-group-item border-0 px-0">
                    <i class="bi bi-3-circle text-primary me-2"></i>
                    Get auto-allocated to first available
                  </div>
                  <div class="list-group-item border-0 px-0">
                    <i class="bi bi-4-circle text-primary me-2"></i>
                    Mark as occupied when you arrive
                  </div>
                  <div class="list-group-item border-0 px-0">
                    <i class="bi bi-5-circle text-primary me-2"></i>
                    Release spot when leaving
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Composables
const router = useRouter();
const authStore = useAuthStore();

// Reactive state
const isLoading = ref(false);

// Mock data for demonstration
const adminStats = ref([
  { id: 1, value: '12', label: 'Parking Lots', icon: 'bi bi-building', color: '#007bff' },
  { id: 2, value: '156', label: 'Total Spots', icon: 'bi bi-grid', color: '#28a745' },
  { id: 3, value: '89', label: 'Active Users', icon: 'bi bi-people', color: '#ffc107' },
  { id: 4, value: '67%', label: 'Occupancy', icon: 'bi bi-pie-chart', color: '#dc3545' }
]);

const userStats = ref([
  { id: 1, value: '3', label: 'Total Bookings', icon: 'bi bi-calendar-check', color: '#007bff' },
  { id: 2, value: '12h', label: 'Total Time', icon: 'bi bi-clock', color: '#28a745' },
  { id: 3, value: '$45', label: 'Total Spent', icon: 'bi bi-currency-dollar', color: '#ffc107' }
]);

const recentActivity = ref([
  { id: 1, description: 'New user registration', time: '2 hours ago', icon: 'bi bi-person-plus' },
  { id: 2, description: 'Parking lot updated', time: '4 hours ago', icon: 'bi bi-building' },
  { id: 3, description: 'System backup completed', time: '6 hours ago', icon: 'bi bi-shield-check' },
  { id: 4, description: 'Payment processed', time: '8 hours ago', icon: 'bi bi-credit-card' }
]);

// Methods
const formatDate = (dateString: string | undefined): string => {
  if (!dateString) return 'Never';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch {
    return 'Invalid date';
  }
};

const refreshData = async (): Promise<void> => {
  isLoading.value = true;
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Refresh user data
    await authStore.checkAuth();
    
    console.log('Dashboard data refreshed');
  } catch (error) {
    console.error('Failed to refresh data:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleProfile = (): void => {
  // Navigate to profile page (to be implemented)
  console.log('Navigate to profile');
};

const handleSettings = (): void => {
  // Navigate to settings page (to be implemented)
  console.log('Navigate to settings');
};

const handleLogout = async (): Promise<void> => {
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

// Lifecycle hooks
onMounted(() => {
  // Check authentication status
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  // Initialize dashboard data
  refreshData();

  // Start token refresh timer
  authStore.startTokenRefreshTimer();
});
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.card {
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-item {
  position: relative;
}

.timeline-item:not(:last-child)::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 25px;
  height: 20px;
  width: 1px;
  background-color: #dee2e6;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.progress {
  border-radius: 10px;
}

.badge {
  font-size: 0.7rem;
}

@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.25rem;
  }
  
  .h3 {
    font-size: 1.5rem;
  }
  
  .display-4 {
    font-size: 2rem;
  }
}
</style> 