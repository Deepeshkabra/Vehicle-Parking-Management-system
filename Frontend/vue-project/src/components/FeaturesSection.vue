<template>
  <section id="features" class="features-section py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-8 mx-auto text-center mb-5">
          <h2 class="display-5 fw-bold mb-4">Powerful Features for Everyone</h2>
          <p class="lead text-muted">
            Our comprehensive parking management solution caters to both administrators and users with 
            intuitive features designed for efficiency and convenience.
          </p>
        </div>
      </div>
      
      <!-- Admin Features -->
      <div class="row mb-5">
        <div class="col-12 mb-4">
          <h3 class="h4 text-primary mb-3">
            <i class="bi bi-shield-check me-2"></i>
            For Administrators
          </h3>
        </div>
        <div class="col-md-6 col-lg-3 mb-4" v-for="feature in adminFeatures" :key="feature.id">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-body text-center p-4">
              <div class="feature-icon mb-3">
                <i :class="feature.icon" class="display-4 text-primary"></i>
              </div>
              <h5 class="card-title">{{ feature.title }}</h5>
              <p class="card-text text-muted">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- User Features -->
      <div class="row">
        <div class="col-12 mb-4">
          <h3 class="h4 text-success mb-3">
            <i class="bi bi-person-check me-2"></i>
            For Users
          </h3>
        </div>
        <div class="col-md-6 col-lg-3 mb-4" v-for="feature in userFeatures" :key="feature.id">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-body text-center p-4">
              <div class="feature-icon mb-3">
                <i :class="feature.icon" class="display-4 text-success"></i>
              </div>
              <h5 class="card-title">{{ feature.title }}</h5>
              <p class="card-text text-muted">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Feature {
  id: number;
  title: string;
  description: string;
  icon: string;
}

const adminFeatures = ref<Feature[]>([
  {
    id: 1,
    title: 'Lot Management',
    description: 'Create, edit, and manage parking lots with automatic spot generation based on capacity.',
    icon: 'bi bi-building'
  },
  {
    id: 2,
    title: 'Real-time Monitoring',
    description: 'Monitor all parking spots in real-time with live status updates and occupancy tracking.',
    icon: 'bi bi-eye'
  },
  {
    id: 3,
    title: 'User Management',
    description: 'Manage registered users, view their parking history, and handle user accounts.',
    icon: 'bi bi-people'
  },
  {
    id: 4,
    title: 'Analytics Dashboard',
    description: 'Comprehensive analytics with charts, reports, and insights into parking patterns.',
    icon: 'bi bi-graph-up'
  }
]);

const userFeatures = ref<Feature[]>([
  {
    id: 1,
    title: 'Easy Booking',
    description: 'Simple and intuitive booking process for finding and reserving parking spots.',
    icon: 'bi bi-calendar-check'
  },
  {
    id: 2,
    title: 'Auto-allocation',
    description: 'Automatic allocation to the first available spot - no need to choose manually.',
    icon: 'bi bi-geo-alt'
  },
  {
    id: 3,
    title: 'History Tracking',
    description: 'Complete parking history with timestamps, costs, and detailed records.',
    icon: 'bi bi-clock-history'
  },
  {
    id: 4,
    title: 'Export & Reports',
    description: 'Export parking details as CSV files and receive automated reports.',
    icon: 'bi bi-file-earmark-spreadsheet'
  }
]);
</script>

<style scoped>
.features-section {
  background-color: #f8f9fa;
}

.feature-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
