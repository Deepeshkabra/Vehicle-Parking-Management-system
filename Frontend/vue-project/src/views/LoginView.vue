<template>
  <div class="login-page d-flex align-items-center justify-content-center min-vh-100 bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <router-link to="/" class="text-decoration-none">
                  <i class="bi bi-car-front text-primary display-4"></i>
                  <h2 class="mt-3 text-primary">ParkingManager</h2>
                </router-link>
                <p class="text-muted">Sign in to your account</p>
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

              <div v-if="successMessage" class="alert alert-success alert-dismissible" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
                <button 
                  type="button" 
                  class="btn-close" 
                  @click="successMessage = ''"
                  aria-label="Close"
                ></button>
              </div>

              <!-- Login Form -->
              <form @submit.prevent="handleLogin" novalidate>
                <!-- Username/Email Field -->
                <div class="mb-3">
                  <label for="username" class="form-label">
                    Username or Email
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
                      :class="{ 'is-invalid': validationErrors.username }"
                      placeholder="Enter username or email"
                      required
                      autocomplete="username"
                    />
                    <div v-if="validationErrors.username" class="invalid-feedback">
                      {{ validationErrors.username }}
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
                      :class="{ 'is-invalid': validationErrors.password }"
                      placeholder="Enter password"
                      required
                      autocomplete="current-password"
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
                </div>

                <!-- Remember Me & Login Type -->
                <div class="row mb-4">
                  <div class="col-6">
                    <div class="form-check">
                      <input
                        id="rememberMe"
                        v-model="form.remember_me"
                        type="checkbox"
                        class="form-check-input"
                      />
                      <label for="rememberMe" class="form-check-label">
                        Remember me
                      </label>
                    </div>
                  </div>
                  <div class="col-6 text-end">
                    <small class="text-muted">
                      <i class="bi bi-info-circle me-1"></i>
                      {{ loginType }}
                    </small>
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
                      Signing in...
                    </div>
                    <div v-else>
                      <i class="bi bi-box-arrow-in-right me-2"></i>
                      Sign In
                    </div>
                  </button>
                </div>
              </form>

              <!-- Admin Info -->
              <div class="alert alert-info mb-3">
                <small>
                  <i class="bi bi-info-circle me-2"></i>
                  <strong>Admin Access:</strong> Use your configured admin credentials to access the admin dashboard.
                </small>
              </div>

              <!-- Register Link -->
              <div class="text-center">
                <p class="mb-0">
                  Don't have an account?
                  <router-link to="/register" class="text-primary text-decoration-none">
                    <strong>Register here</strong>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import type { LoginCredentials } from '@/services/authService';

// Composables
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// Reactive state
const form = ref<LoginCredentials>({
  username: '',
  password: '',
  remember_me: false
});

const showPassword = ref(false);
const successMessage = ref('');
const validationErrors = ref<Record<string, string>>({});

// Computed properties
const isFormValid = computed(() => {
  return form.value.username.trim() !== '' && 
         form.value.password.trim() !== '' && 
         Object.keys(validationErrors.value).length === 0;
});

const loginType = computed(() => {
  const username = form.value.username.toLowerCase();
  if (username.includes('admin') || username === 'admin@example.com') {
    return 'Admin Login';
  }
  return 'User Login';
});

// Methods
const validateForm = (): boolean => {
  validationErrors.value = {};
  
  const errors = authStore.validateLoginForm(form.value);
  
  if (errors.length > 0) {
    // Map generic errors to specific fields
    errors.forEach(error => {
      if (error.includes('Username') || error.includes('email')) {
        validationErrors.value.username = error;
      } else if (error.includes('Password')) {
        validationErrors.value.password = error;
      }
    });
    return false;
  }
  
  return true;
};

const handleLogin = async (): Promise<void> => {
  // Clear previous errors
  authStore.clearError();
  validationErrors.value = {};
  
  // Validate form
  if (!validateForm()) {
    return;
  }
  
  try {
    await authStore.login(form.value);
    
    // Success - redirect based on user role
    const redirectTo = (route.query.redirect as string) || getDefaultRedirect();
    
    successMessage.value = `Welcome back, ${authStore.userName}!`;
    
    // Small delay to show success message
    setTimeout(() => {
      router.push(redirectTo);
    }, 1000);
    
  } catch (error) {
    // Error is handled by the store, just scroll to top to show error
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
};

const getDefaultRedirect = (): string => {
  if (authStore.isAdmin) {
    return '/admin';
  } else if (authStore.isUser) {
    return '/dashboard';
  }
  return '/';
};

// Lifecycle hooks
onMounted(() => {
  // If already authenticated, redirect
  if (authStore.isAuthenticated) {
    const redirectTo = (route.query.redirect as string) || getDefaultRedirect();
    router.replace(redirectTo);
  }
  
  // Check for success message from registration
  if (route.query.registered === 'true') {
    successMessage.value = 'Registration successful! Please sign in.';
  }
  
  // Pre-fill username if provided via route query
  if (route.query.username) {
    form.value.username = route.query.username as string;
  }
});
</script>

<style scoped>
.login-page {
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

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

@media (max-width: 576px) {
  .card-body {
    padding: 2rem !important;
  }
  
  .display-4 {
    font-size: 2rem;
  }
}
</style>