<template>
  <footer class="footer-section bg-dark text-white py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-4 mb-4">
          <h5 class="mb-4">
            <i class="bi bi-car-front me-2"></i>
            Vehicle Parking Management
          </h5>
          <p class="text-muted">
            Smart parking solutions designed for modern cities. Efficient, user-friendly, 
            and built with the latest technology to make parking management effortless.
          </p>
          <div class="social-links">
            <a href="#" class="text-white me-3">
              <i class="bi bi-facebook"></i>
            </a>
            <a href="#" class="text-white me-3">
              <i class="bi bi-twitter"></i>
            </a>
            <a href="#" class="text-white me-3">
              <i class="bi bi-linkedin"></i>
            </a>
            <a href="#" class="text-white">
              <i class="bi bi-github"></i>
            </a>
          </div>
        </div>
        
        <div class="col-lg-2 col-md-6 mb-4">
          <h6 class="mb-4">Features</h6>
          <ul class="list-unstyled">
            <li class="mb-2">
              <a href="#features" class="text-muted text-decoration-none">Admin Tools</a>
            </li>
            <li class="mb-2">
              <a href="#features" class="text-muted text-decoration-none">User Interface</a>
            </li>
            <li class="mb-2">
              <a href="#features" class="text-muted text-decoration-none">Real-time Tracking</a>
            </li>
            <li class="mb-2">
              <a href="#features" class="text-muted text-decoration-none">Analytics</a>
            </li>
          </ul>
        </div>
        
        <div class="col-lg-2 col-md-6 mb-4">
          <h6 class="mb-4">How It Works</h6>
          <ul class="list-unstyled">
            <li class="mb-2">
              <a href="#how-it-works" class="text-muted text-decoration-none">For Admins</a>
            </li>
            <li class="mb-2">
              <a href="#how-it-works" class="text-muted text-decoration-none">For Users</a>
            </li>
            <li class="mb-2">
              <a href="#how-it-works" class="text-muted text-decoration-none">Auto-allocation</a>
            </li>
            <li class="mb-2">
              <a href="#how-it-works" class="text-muted text-decoration-none">Payments</a>
            </li>
          </ul>
        </div>
        
        <div class="col-lg-2 col-md-6 mb-4">
          <h6 class="mb-4">Support</h6>
          <ul class="list-unstyled">
            <li class="mb-2">
              <a href="#contact" class="text-muted text-decoration-none">Contact Us</a>
            </li>
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">Help Center</a>
            </li>
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">Documentation</a>
            </li>
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">API Reference</a>
            </li>
          </ul>
        </div>
        
        <div class="col-lg-2 col-md-6 mb-4">
          <h6 class="mb-4">Company</h6>
          <ul class="list-unstyled">
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">About Us</a>
            </li>
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">Privacy Policy</a>
            </li>
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">Terms of Service</a>
            </li>
            <li class="mb-2">
              <a href="#" class="text-muted text-decoration-none">Careers</a>
            </li>
          </ul>
        </div>
      </div>
      
      <hr class="my-4">
      
      <div class="row align-items-center">
        <div class="col-md-6">
          <p class="text-muted mb-0">
            © 2024 Vehicle Parking Management System. All rights reserved.
          </p>
        </div>
        <div class="col-md-6 text-md-end">
          <p class="text-muted mb-0">
            Built with Vue.js, Bootstrap & Modern Web Technologies
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component logic can be added here if needed
</script>

<style scoped>
.footer-section {
  background-color: #212529 !important;
}

.social-links a {
  font-size: 1.25rem;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: #007bff !important;
}

.list-unstyled a:hover {
  color: #007bff !important;
}
</style>
