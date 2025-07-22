<template>
  <section id="benefits" class="benefits-section py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-8 mx-auto text-center mb-5">
          <h2 class="display-5 fw-bold mb-4">Why Choose Our System?</h2>
          <p class="lead text-muted">
            Experience the advantages of modern parking management with our comprehensive solution.
          </p>
        </div>
      </div>
      
      <div class="row">
        <div class="col-lg-6 mb-4" v-for="benefit in benefits" :key="benefit.id">
          <div class="benefit-card h-100 p-4 border-0 shadow-sm">
            <div class="d-flex align-items-start">
              <div class="benefit-icon me-4">
                <i :class="benefit.icon" class="display-4" :style="{ color: benefit.color }"></i>
              </div>
              <div>
                <h4 class="mb-3">{{ benefit.title }}</h4>
                <p class="text-muted mb-3">{{ benefit.description }}</p>
                <ul class="list-unstyled">
                  <li v-for="feature in benefit.features" :key="feature" class="mb-2">
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    {{ feature }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Stats Section -->
      <div class="row mt-5">
        <div class="col-12 mb-4">
          <h3 class="h4 text-center mb-4">System Performance</h3>
        </div>
        <div class="col-md-3 col-6 mb-4" v-for="stat in stats" :key="stat.id">
          <div class="stat-card text-center p-4">
            <div class="stat-icon mb-3">
              <i :class="stat.icon" class="display-4 text-primary"></i>
            </div>
            <h3 class="fw-bold text-primary mb-1">{{ stat.value }}</h3>
            <p class="text-muted mb-0">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Benefit {
  id: number;
  title: string;
  description: string;
  icon: string;
  color: string;
  features: string[];
}

interface Stat {
  id: number;
  value: string;
  label: string;
  icon: string;
}

const benefits = ref<Benefit[]>([
  {
    id: 1,
    title: 'Efficiency & Automation',
    description: 'Streamline your parking operations with intelligent automation and real-time updates.',
    icon: 'bi bi-lightning-charge',
    color: '#ffc107',
    features: [
      'Auto-allocation system',
      'Real-time spot tracking',
      'Instant notifications',
      'Automated reporting'
    ]
  },
  {
    id: 2,
    title: 'Easy Management',
    description: 'Comprehensive admin tools and user-friendly interface for effortless management.',
    icon: 'bi bi-gear',
    color: '#6c757d',
    features: [
      'Intuitive dashboard',
      'User management',
      'Lot configuration',
      'Analytics & insights'
    ]
  },
  {
    id: 3,
    title: 'Superior User Experience',
    description: 'Designed with both administrators and users in mind for optimal usability.',
    icon: 'bi bi-heart',
    color: '#e83e8c',
    features: [
      'Simple booking process',
      'Mobile responsive',
      'History tracking',
      'Export capabilities'
    ]
  },
  {
    id: 4,
    title: 'Modern Technology',
    description: 'Built with cutting-edge web technologies for reliability and performance.',
    icon: 'bi bi-cpu',
    color: '#20c997',
    features: [
      'Real-time updates',
      'Secure authentication',
      'Background processing',
      'Cross-platform support'
    ]
  }
]);

const stats = ref<Stat[]>([
  {
    id: 1,
    value: '99.9%',
    label: 'Uptime',
    icon: 'bi bi-graph-up'
  },
  {
    id: 2,
    value: '<3s',
    label: 'Response Time',
    icon: 'bi bi-speedometer'
  },
  {
    id: 3,
    value: '24/7',
    label: 'Support',
    icon: 'bi bi-headset'
  },
  {
    id: 4,
    value: '100%',
    label: 'Secure',
    icon: 'bi bi-shield-check'
  }
]);
</script>

<style scoped>
.benefits-section {
  background-color: #f8f9fa;
}

.benefit-card {
  background-color: white;
  border-radius: 15px;
  transition: transform 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
}

.benefit-icon {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 50%;
  flex-shrink: 0;
}

.stat-card {
  background-color: white;
  border-radius: 15px;
  border: 1px solid #e9ecef;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
