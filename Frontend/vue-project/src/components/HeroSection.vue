<template>
  <section class="hero-section bg-primary text-white py-5">
    <div class="container">
      <div class="row align-items-center min-vh-100">
        <div class="col-lg-6 fade-in-up">
          <h1 class="display-4 fw-bold mb-4">
            Smart Parking Management Made Simple
          </h1>
          <p class="lead mb-4">
            Revolutionize your parking experience with our intelligent management system. 
            Auto-allocation, real-time monitoring, and seamless user experience for both 
            administrators and users.
          </p>
          <div class="mb-4">
            <div class="row">
              <div class="col-sm-6 mb-2">
                <i class="bi bi-check-circle-fill text-warning me-2"></i>
                <span>Real-time availability</span>
              </div>
              <div class="col-sm-6 mb-2">
                <i class="bi bi-check-circle-fill text-warning me-2"></i>
                <span>Auto-allocation system</span>
              </div>
              <div class="col-sm-6 mb-2">
                <i class="bi bi-check-circle-fill text-warning me-2"></i>
                <span>Mobile responsive</span>
              </div>
              <div class="col-sm-6 mb-2">
                <i class="bi bi-check-circle-fill text-warning me-2"></i>
                <span>Admin dashboard</span>
              </div>
            </div>
          </div>
          <div class="d-flex gap-3 flex-wrap">
            <button class="btn btn-dark btn-lg px-4" @click="scrollToSection('features')">
              <i class="bi bi-arrow-right me-2"></i>
              Learn More
            </button>
            <button class="btn btn-outline-light btn-lg px-4" @click="scrollToSection('contact')">
              <i class="bi bi-play-circle me-2"></i>
              Get Started
            </button>
          </div>
        </div>
        <div class="col-lg-6 text-center fade-in-up">
          <div class="hero-image-container">
            <div class="hero-image-placeholder bg-light bg-opacity-90 rounded-3 p-5 position-relative">
              <div class="hero-icon-grid">
                <i class="bi bi-car-front display-1 text-primary mb-3"></i>
                <div class="row">
                  <div class="col-4">
                    <i class="bi bi-geo-alt text-warning fs-2"></i>
                  </div>
                  <div class="col-4">
                    <i class="bi bi-clock text-info fs-2"></i>
                  </div>
                  <div class="col-4">
                    <i class="bi bi-shield-check text-success fs-2"></i>
                  </div>
                </div>
              </div>
              <h3 class="mt-3 text-dark">Smart Parking System</h3>
              <p class="mb-0 text-dark">Auto-allocation • Real-time Updates • Easy Management</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
};
</script>

<style scoped>
.hero-image-placeholder {
  min-height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.hero-image-placeholder:hover {
  transform: scale(1.02);
}

@media (max-width: 768px) {
  .hero-section {
    padding: 3rem 0;
  }
  
  .min-vh-100 {
    min-height: auto;
  }
  
  .hero-image-placeholder {
    min-height: 250px;
  }
}
</style>