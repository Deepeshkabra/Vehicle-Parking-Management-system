<template>
    <div class="home-container">
      <div class="container-fluid">
        <div class="row justify-content-center">
          <div class="col-md-8 col-lg-6 text-center">
            <div class="welcome-card">
              <div class="card border-0 shadow-lg">
                <div class="card-body p-5">
                  <div class="mb-4">
                    <i class="fas fa-parking fa-4x text-primary mb-3"></i>
                  </div>
                  <h1 class="display-4 fw-bold text-primary mb-3">
                    Welcome to Parking Management System
                  </h1>
                  <p class="lead text-muted mb-4">
                    Efficiently manage your parking spaces and reservations with our comprehensive parking management solution.
                  </p>
                  <div class="d-grid gap-2 d-md-block">
                    <router-link 
                      to="/login" 
                      class="btn btn-primary btn-lg me-md-2"
                    >
                      <i class="fas fa-sign-in-alt me-2"></i>
                      Login
                    </router-link>
                    <router-link 
                      to="/register" 
                      class="btn btn-outline-primary btn-lg"
                    >
                      <i class="fas fa-user-plus me-2"></i>
                      Register
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Features Section -->
        <div class="row justify-content-center mt-5">
          <div class="col-md-10">
            <div class="row g-4">
              <div class="col-md-4">
                <div class="text-center">
                  <div class="feature-icon">
                    <i class="fas fa-car fa-2x text-primary mb-3"></i>
                  </div>
                  <h5>Easy Parking</h5>
                  <p class="text-muted">Find and reserve parking spots quickly and efficiently</p>
                </div>
              </div>
              <div class="col-md-4">
                <div class="text-center">
                  <div class="feature-icon">
                    <i class="fas fa-clock fa-2x text-primary mb-3"></i>
                  </div>
                  <h5>Real-time Availability</h5>
                  <p class="text-muted">Check live parking spot availability across all locations</p>
                </div>
              </div>
              <div class="col-md-4">
                <div class="text-center">
                  <div class="feature-icon">
                    <i class="fas fa-shield-alt fa-2x text-primary mb-3"></i>
                  </div>
                  <h5>Secure Management</h5>
                  <p class="text-muted">Secure and reliable parking management for peace of mind</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  
  const router = useRouter()
  const authStore = useAuthStore()
  
  // Redirect authenticated users to their dashboard
  onMounted(() => {
    if (authStore.isLoggedIn) {
      if (authStore.user?.role === 'admin') {
        router.push('/admin/dashboard')
      } else {
        router.push('/user/dashboard')
      }
    }
  })
  </script>
  
  <style scoped>
  .home-container {
    min-height: calc(100vh - 76px); /* Adjust based on your navbar height */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60px 0;
  }
  
  .welcome-card {
    animation: fadeInUp 0.8s ease-out;
  }
  
  .feature-icon {
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .card {
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95);
  }
  
  .btn-lg {
    padding: 12px 30px;
    font-weight: 500;
  }
  
  @media (max-width: 768px) {
    .home-container {
      padding: 40px 0;
    }
    
    .display-4 {
      font-size: 2rem;
    }
    
    .d-grid .btn {
      margin-bottom: 10px;
    }
  }
  </style>