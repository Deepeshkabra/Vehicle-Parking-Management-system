<template>
  <section id="contact" class="contact-section py-5">
    <div class="container">
      <div class="row">
        <div class="col-lg-8 mx-auto text-center mb-5">
          <h2 class="display-5 fw-bold mb-4">Get Started Today</h2>
          <p class="lead text-muted">
            Ready to revolutionize your parking management? Contact us for a demo or get started with our system.
          </p>
        </div>
      </div>
      
      <div class="row">
        <div class="col-lg-8 mx-auto">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <form @submit.prevent="handleSubmit">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="name" class="form-label">Full Name *</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="name" 
                      v-model="form.name"
                      required
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label">Email Address *</label>
                    <input 
                      type="email" 
                      class="form-control" 
                      id="email" 
                      v-model="form.email"
                      required
                    >
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="organization" class="form-label">Organization</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="organization" 
                      v-model="form.organization"
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="userType" class="form-label">I am interested as:</label>
                    <select class="form-select" id="userType" v-model="form.userType">
                      <option value="">Select option</option>
                      <option value="admin">Administrator</option>
                      <option value="user">End User</option>
                      <option value="both">Both</option>
                    </select>
                  </div>
                </div>
                <div class="mb-4">
                  <label for="message" class="form-label">Message</label>
                  <textarea 
                    class="form-control" 
                    id="message" 
                    rows="4" 
                    v-model="form.message"
                    placeholder="Tell us about your parking management needs..."
                  ></textarea>
                </div>
                <div class="d-grid">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg"
                    :disabled="isSubmitting"
                  >
                    <i class="bi bi-send me-2"></i>
                    {{ isSubmitting ? 'Sending...' : 'Request Demo' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Contact Info -->
      <div class="row mt-5">
        <div class="col-lg-4 mb-4" v-for="contact in contactInfo" :key="contact.id">
          <div class="contact-card text-center p-4">
            <div class="contact-icon mb-3">
              <i :class="contact.icon" class="display-4 text-primary"></i>
            </div>
            <h5 class="mb-3">{{ contact.title }}</h5>
            <p class="text-muted mb-0">{{ contact.info }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

interface ContactInfo {
  id: number;
  title: string;
  info: string;
  icon: string;
}

const isSubmitting = ref(false);

const form = reactive({
  name: '',
  email: '',
  organization: '',
  userType: '',
  message: ''
});

const contactInfo = ref<ContactInfo[]>([
  {
    id: 1,
    title: 'Email Support',
    info: 'support@parkingmanagement.com',
    icon: 'bi bi-envelope'
  },
  {
    id: 2,
    title: 'Phone Support',
    info: '+1 (555) 123-4567',
    icon: 'bi bi-telephone'
  },
  {
    id: 3,
    title: 'Live Chat',
    info: 'Available 24/7',
    icon: 'bi bi-chat-dots'
  }
]);

const handleSubmit = async () => {
  isSubmitting.value = true;
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Reset form
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = '';
    });
    
    alert('Thank you for your interest! We will contact you soon.');
  } catch (error) {
    alert('There was an error sending your message. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.contact-section {
  background-color: #ffffff;
}

.contact-card {
  background-color: #f8f9fa;
  border-radius: 15px;
  transition: transform 0.3s ease;
}

.contact-card:hover {
  transform: translateY(-5px);
}

.contact-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-control:focus, .form-select:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>
