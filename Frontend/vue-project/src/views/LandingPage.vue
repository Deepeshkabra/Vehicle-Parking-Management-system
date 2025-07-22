<template>
  <div class="landing-page">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container">
        <a class="navbar-brand" href="#">
          <i class="bi bi-car-front me-2"></i>
          ParkingManager
        </a>
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#features">Features</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#how-it-works">How It Works</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#benefits">Benefits</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#contact">Contact</a>
            </li>
            <li class="nav-item">
              <a class="nav-link btn btn-outline-light ms-2 px-3" href="/login">
                <i class="bi bi-box-arrow-in-right me-1"></i>
                Login
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <HeroSection />
    <FeaturesSection />
    <HowItWorksSection />
    <BenefitsSection />
    <ContactSection />
    <FooterSection />
  </div>
</template>

<script setup lang="ts">
import HeroSection from '@/components/HeroSection.vue';
import FeaturesSection from '@/components/FeaturesSection.vue';
import HowItWorksSection from '@/components/HowItWorksSection.vue';
import BenefitsSection from '@/components/BenefitsSection.vue';
import ContactSection from '@/components/ContactSection.vue';
import FooterSection from '@/components/FooterSection.vue';

// Add smooth scrolling for navbar links
document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.navbar-nav a[href^="#"]');
  
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href') || '');
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});
</script>

<style scoped>
.landing-page {
  padding-top: 0;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
}

.nav-link {
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: #fff !important;
}

/* Smooth scroll behavior */
html {
  scroll-behavior: smooth;
}

/* Add padding to sections to account for fixed navbar */
section {
  scroll-margin-top: 70px;
}
</style>
