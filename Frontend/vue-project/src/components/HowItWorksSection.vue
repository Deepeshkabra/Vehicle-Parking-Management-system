<template>
  <section id="how-it-works" class="how-it-works-section py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-8 mx-auto text-center mb-5">
          <h2 class="display-5 fw-bold mb-4">How It Works</h2>
          <p class="lead text-muted">
            Our streamlined process makes parking management effortless for both administrators and users.
          </p>
        </div>
      </div>
      
      <!-- Admin Workflow -->
      <div class="row mb-5">
        <div class="col-12 mb-4">
          <h3 class="h4 text-primary mb-3">
            <i class="bi bi-shield-check me-2"></i>
            Admin Workflow
          </h3>
        </div>
        <div class="col-md-6 col-lg-3 mb-4" v-for="(step, index) in adminSteps" :key="step.id">
          <div class="step-card text-center">
            <div class="step-number mb-3">{{ index + 1 }}</div>
            <div class="step-icon mb-3">
              <i :class="step.icon" class="display-4 text-primary"></i>
            </div>
            <h5 class="mb-3">{{ step.title }}</h5>
            <p class="text-muted">{{ step.description }}</p>
          </div>
        </div>
      </div>
      
      <!-- User Workflow -->
      <div class="row">
        <div class="col-12 mb-4">
          <h3 class="h4 text-success mb-3">
            <i class="bi bi-person-check me-2"></i>
            User Workflow
          </h3>
        </div>
        <div class="col-md-6 col-lg-3 mb-4" v-for="(step, index) in userSteps" :key="step.id">
          <div class="step-card text-center">
            <div class="step-number mb-3 bg-success">{{ index + 1 }}</div>
            <div class="step-icon mb-3">
              <i :class="step.icon" class="display-4 text-success"></i>
            </div>
            <h5 class="mb-3">{{ step.title }}</h5>
            <p class="text-muted">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Step {
  id: number;
  title: string;
  description: string;
  icon: string;
}

const adminSteps = ref<Step[]>([
  {
    id: 1,
    title: 'Create Parking Lots',
    description: 'Set up parking lots with location details, pricing, and capacity information.',
    icon: 'bi bi-plus-circle'
  },
  {
    id: 2,
    title: 'Monitor in Real-time',
    description: 'Track all parking spots, occupancy status, and user activities in real-time.',
    icon: 'bi bi-display'
  },
  {
    id: 3,
    title: 'Manage Users',
    description: 'Handle user registrations, view parking history, and manage user accounts.',
    icon: 'bi bi-person-gear'
  },
  {
    id: 4,
    title: 'Generate Reports',
    description: 'Access comprehensive analytics, generate reports, and export data.',
    icon: 'bi bi-file-text'
  }
]);

const userSteps = ref<Step[]>([
  {
    id: 1,
    title: 'Find Available Lots',
    description: 'Browse available parking lots and view real-time availability and pricing.',
    icon: 'bi bi-search'
  },
  {
    id: 2,
    title: 'Auto-allocation',
    description: 'Get automatically assigned to the first available spot in your chosen lot.',
    icon: 'bi bi-geo-alt-fill'
  },
  {
    id: 3,
    title: 'Park & Mark Occupied',
    description: 'Arrive at your assigned spot and mark it as occupied through the app.',
    icon: 'bi bi-car-front-fill'
  },
  {
    id: 4,
    title: 'Release & Pay',
    description: 'Mark your spot as released when leaving and complete the payment process.',
    icon: 'bi bi-credit-card'
  }
]);
</script>

<style scoped>
.how-it-works-section {
  background-color: #ffffff;
}

.step-card {
  padding: 2rem 1rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.step-card:hover {
  background-color: #f8f9fa;
  transform: translateY(-5px);
}

.step-number {
  width: 50px;
  height: 50px;
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  margin: 0 auto;
}

.step-number.bg-success {
  background-color: #28a745 !important;
}

.step-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
