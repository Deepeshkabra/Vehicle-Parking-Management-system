<template>
  <div class="register-page d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <router-link to="/" class="text-decoration-none">
                  <i class="bi bi-car-front text-primary display-4"></i>
                  <h2 class="mt-3 text-primary">ParkingManager</h2>
                </router-link>
                <p class="text-muted">Create your account</p>
              </div>

              <!-- Alert Messages -->
              <div v-if="authStore.error" class="alert alert-danger alert-dismissible" role="alert">
                <i class="bi bi-exclamation-circle me-2"></i>
                {{ authStore.error }}
                <button 
                  type="button" 
                  class="btn-close" 
                  @click="authStore.clearError()"
                  aria-label="Close"
                ></button>
              </div>

              <!-- Registration Form -->
              <form @submit.prevent="handleRegister" novalidate>
                <div class="row">
                  <!-- Username Field -->
                  <div class="col-md-6 mb-3">
                    <label for="username" class="form-label">
                      Username
                      <span class="text-danger">*</span>
                    </label>
                    <div class="input-group">
                      <span class="input-group-text">
                        <i class="bi bi-person"></i>
                      </span>
                      <input
                        id="username"
                        v-model="form.username"
                        type="text"
                        class="form-control"
                        :class="{ 
                          'is-invalid': validationErrors.username,
                          'is-valid': form.username && !validationErrors.username && usernameValidation.isValid
                        }"
                        placeholder="Choose a username"
                        required
                        autocomplete="username"
                        @blur="validateUsername"
                        @input="realTimeValidateUsername"
                      />
                      <div v-if="validationErrors.username" class="invalid-feedback">
                        {{ validationErrors.username }}
                      </div>
                      <div v-else-if="form.username && usernameValidation.isValid" class="valid-feedback">
                        Username is available
                      </div>
                    </div>
                    <small v-if="usernameValidation.errors.length > 0" class="text-muted">
                      <ul class="mb-0 ps-3">
                        <li v-for="error in usernameValidation.errors" :key="error" class="small">
                          {{ error }}
                        </li>
                      </ul>
                    </small>
                  </div>

                  <!-- Email Field -->
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label">
                      Email Address
                      <span class="text-danger">*</span>
                    </label>
                    <div class="input-group">
                      <span class="input-group-text">
                        <i class="bi bi-envelope"></i>
                      </span>
                      <input
                        id="email"
                        v-model="form.email"
                        type="email"
                        class="form-control"
                        :class="{ 
                          'is-invalid': validationErrors.email,
                          'is-valid': form.email && !validationErrors.email && isValidEmail
                        }"
                        placeholder="Enter your email"
                        required
                        autocomplete="email"
                        @blur="validateEmail"
                      />
                      <div v-if="validationErrors.email" class="invalid-feedback">
                        {{ validationErrors.email }}
                      </div>
                      <div v-else-if="form.email && isValidEmail" class="valid-feedback">
                        Email format is valid
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Phone Field -->
                <div class="mb-3">
                  <label for="phone" class="form-label">
                    Phone Number
                    <small class="text-muted">(optional)</small>
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-telephone"></i>
                    </span>
                    <input
                      id="phone"
                      v-model="form.phone"
                      type="tel"
                      class="form-control"
                      :class="{ 'is-invalid': validationErrors.phone }"
                      placeholder="Enter your phone number"
                      autocomplete="tel"
                    />
                    <div v-if="validationErrors.phone" class="invalid-feedback">
                      {{ validationErrors.phone }}
                    </div>
                  </div>
                </div>

                <!-- Password Field -->
                <div class="mb-3">
                  <label for="password" class="form-label">
                    Password
                    <span class="text-danger">*</span>
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input
                      id="password"
                      v-model="form.password"
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      :class="{ 
                        'is-invalid': validationErrors.password,
                        'is-valid': form.password && passwordStrength.isValid
                      }"
                      placeholder="Create a strong password"
                      required
                      autocomplete="new-password"
                      @input="updatePasswordStrength"
                    />
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                      tabindex="-1"
                    >
                      <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                    <div v-if="validationErrors.password" class="invalid-feedback">
                      {{ validationErrors.password }}
                    </div>
                  </div>
                  
                  <!-- Password Strength Indicator -->
                  <div v-if="form.password" class="mt-2">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <small class="text-muted">Password Strength:</small>
                      <small :class="strengthColorClass">{{ passwordStrength.strength.toUpperCase() }}</small>
                    </div>
                    <div class="progress" style="height: 4px;">
                      <div 
                        class="progress-bar" 
                        :class="strengthColorClass.replace('text-', 'bg-')"
                        :style="{ width: strengthPercentage + '%' }"
                      ></div>
                    </div>
                    <div v-if="passwordStrength.errors.length > 0" class="mt-1">
                      <small class="text-muted">Requirements:</small>
                      <ul class="small text-muted mb-0 ps-3">
                        <li v-for="error in passwordStrength.errors" :key="error">
                          {{ error }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <!-- Confirm Password Field -->
                <div class="mb-4">
                  <label for="confirmPassword" class="form-label">
                    Confirm Password
                    <span class="text-danger">*</span>
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-lock-fill"></i>
                    </span>
                    <input
                      id="confirmPassword"
                      v-model="confirmPassword"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-control"
                      :class="{ 
                        'is-invalid': validationErrors.confirmPassword,
                        'is-valid': confirmPassword && passwordsMatch
                      }"
                      placeholder="Confirm your password"
                      required
                      autocomplete="new-password"
                    />
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showConfirmPassword = !showConfirmPassword"
                      tabindex="-1"
                    >
                      <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                    <div v-if="validationErrors.confirmPassword" class="invalid-feedback">
                      {{ validationErrors.confirmPassword }}
                    </div>
                    <div v-else-if="confirmPassword && passwordsMatch" class="valid-feedback">
                      Passwords match
                    </div>
                  </div>
                </div>

                <!-- Terms and Conditions -->
                <div class="mb-4">
                  <div class="form-check">
                    <input
                      id="agreeTerms"
                      v-model="agreeTerms"
                      type="checkbox"
                      class="form-check-input"
                      :class="{ 'is-invalid': validationErrors.terms }"
                      required
                    />
                    <label for="agreeTerms" class="form-check-label">
                      I agree to the 
                      <a href="#" class="text-primary" @click.prevent="showTerms = true">
                        Terms and Conditions
                      </a> 
                      and 
                      <a href="#" class="text-primary" @click.prevent="showPrivacy = true">
                        Privacy Policy
                      </a>
                      <span class="text-danger">*</span>
                    </label>
                    <div v-if="validationErrors.terms" class="invalid-feedback">
                      {{ validationErrors.terms }}
                    </div>
                  </div>
                </div>

                <!-- Submit Button -->
                <div class="d-grid mb-3">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="authStore.isLoading || !isFormValid"
                  >
                    <div v-if="authStore.isLoading" class="d-flex align-items-center justify-content-center">
                      <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                      </div>
                      Creating account...
                    </div>
                    <div v-else>
                      <i class="bi bi-person-plus me-2"></i>
                      Create Account
                    </div>
                  </button>
                </div>
              </form>

              <!-- Login Link -->
              <div class="text-center">
                <p class="mb-0">
                  Already have an account?
                  <router-link to="/login" class="text-primary text-decoration-none">
                    <strong>Sign in here</strong>
                  </router-link>
                </p>
              </div>

              <!-- Back to Home -->
              <div class="text-center mt-3">
                <router-link to="/" class="btn btn-outline-secondary btn-sm">
                  <i class="bi bi-arrow-left me-2"></i>
                  Back to Home
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Admin Note Modal -->
    <div v-if="showAdminNote" class="modal show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-info-circle text-info me-2"></i>
              Admin Account Information
            </h5>
            <button type="button" class="btn-close" @click="showAdminNote = false"></button>
          </div>
          <div class="modal-body">
            <p>Admin accounts cannot be created through this registration form.</p>
            <p class="mb-0">
              <strong>Admin Access:</strong> Admin users are pre-configured in the system. 
              Please contact your system administrator for admin credentials.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="showAdminNote = false">
              Got it
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import authService, { type RegisterCredentials } from '@/services/authService';

// Composables
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// Reactive state
const form = ref<RegisterCredentials>({
  username: '',
  email: '',
  password: '',
  phone: ''
});

const confirmPassword = ref('');
const agreeTerms = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const showAdminNote = ref(false);
const showTerms = ref(false);
const showPrivacy = ref(false);
const validationErrors = ref<Record<string, string>>({});

// Computed properties
const usernameValidation = computed(() => {
  if (!form.value.username) {
    return { isValid: false, errors: [] };
  }
  return authService.validateUsername(form.value.username);
});

const isValidEmail = computed(() => {
  return form.value.email ? authService.validateEmail(form.value.email) : false;
});

const passwordStrength = computed(() => {
  if (!form.value.password) {
    return { isValid: false, errors: [], strength: 'weak' as const };
  }
  return authStore.getPasswordStrength(form.value.password);
});

const strengthPercentage = computed(() => {
  switch (passwordStrength.value.strength) {
    case 'weak': return 25;
    case 'medium': return 60;
    case 'strong': return 100;
    default: return 0;
  }
});

const strengthColorClass = computed(() => {
  switch (passwordStrength.value.strength) {
    case 'weak': return 'text-danger';
    case 'medium': return 'text-warning';
    case 'strong': return 'text-success';
    default: return 'text-muted';
  }
});

const passwordsMatch = computed(() => {
  return form.value.password && confirmPassword.value && 
         form.value.password === confirmPassword.value;
});

const isFormValid = computed(() => {
  return form.value.username.trim() !== '' && 
         form.value.email.trim() !== '' && 
         form.value.password.trim() !== '' && 
         confirmPassword.value.trim() !== '' &&
         passwordsMatch.value &&
         passwordStrength.value.isValid &&
         usernameValidation.value.isValid &&
         isValidEmail.value &&
         agreeTerms.value &&
         Object.keys(validationErrors.value).length === 0;
});

// Methods
const realTimeValidateUsername = (): void => {
  if (validationErrors.value.username) {
    delete validationErrors.value.username;
  }
};

const validateUsername = (): void => {
  if (!usernameValidation.value.isValid && form.value.username) {
    validationErrors.value.username = usernameValidation.value.errors[0];
  } else {
    delete validationErrors.value.username;
  }
};

const validateEmail = (): void => {
  if (form.value.email && !isValidEmail.value) {
    validationErrors.value.email = 'Please enter a valid email address';
  } else {
    delete validationErrors.value.email;
  }
};

const updatePasswordStrength = (): void => {
  if (validationErrors.value.password) {
    delete validationErrors.value.password;
  }
  
  // Validate confirm password if it exists
  if (confirmPassword.value && !passwordsMatch.value) {
    validationErrors.value.confirmPassword = 'Passwords do not match';
  } else {
    delete validationErrors.value.confirmPassword;
  }
};

const validateForm = (): boolean => {
  validationErrors.value = {};
  
  const errors = authStore.validateRegisterForm(form.value);
  
  if (errors.length > 0) {
    errors.forEach(error => {
      if (error.includes('Username')) {
        validationErrors.value.username = error;
      } else if (error.includes('Email') || error.includes('email')) {
        validationErrors.value.email = error;
      } else if (error.includes('Password')) {
        validationErrors.value.password = error;
      }
    });
  }
  
  // Validate confirm password
  if (!passwordsMatch.value) {
    validationErrors.value.confirmPassword = 'Passwords do not match';
  }
  
  // Validate terms agreement
  if (!agreeTerms.value) {
    validationErrors.value.terms = 'You must agree to the terms and conditions';
  }
  
  return Object.keys(validationErrors.value).length === 0;
};

const handleRegister = async (): Promise<void> => {
  // Clear previous errors
  authStore.clearError();
  validationErrors.value = {};
  
  // Validate form
  if (!validateForm()) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    return;
  }
  
  try {
    await authStore.register(form.value);
    
    // Success - redirect to login with success message
    router.push({ 
      path: '/login', 
      query: { 
        registered: 'true',
        username: form.value.username 
      } 
    });
    
  } catch (error) {
    // Error is handled by the store, just scroll to top to show error
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

// Lifecycle hooks
onMounted(() => {
  // If already authenticated, redirect
  if (authStore.isAuthenticated) {
    router.replace('/dashboard');
  }
  
  // Show admin note if coming from admin-related route
  if (route.query.admin === 'true') {
    showAdminNote.value = true;
  }
});
</script>

<style scoped>
.register-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.card {
  border-radius: 15px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.form-control:focus,
.form-check-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.input-group .form-control {
  border-left: none;
}

.input-group .form-control:focus {
  box-shadow: none;
}

.alert {
  border-radius: 8px;
  border: none;
}

.progress {
  border-radius: 2px;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.modal.show {
  display: flex !important;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .card-body {
    padding: 2rem !important;
  }
  
  .display-4 {
    font-size: 2rem;
  }
  
  .col-md-6 {
    margin-bottom: 1rem;
  }
}
</style> 