<template>
  <div class="min-vh-100 d-flex align-items-center bg-light">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <i class="fas fa-car text-primary mb-3" style="font-size: 3rem;"></i>
                <h2 class="card-title fw-bold text-dark">Welcome Back</h2>
                <p class="text-muted">Sign in to your ParkEase account</p>
              </div>

              <!-- Error Alert -->
              <div 
                v-if="errorMessage" 
                class="alert alert-danger alert-dismissible fade show" 
                role="alert"
              >
                <i class="fas fa-exclamation-triangle me-2"></i>
                {{ errorMessage }}
                <button 
                  type="button" 
                  class="btn-close" 
                  @click="errorMessage = ''"
                  aria-label="Close"
                ></button>
              </div>

              <!-- Success Alert -->
              <div 
                v-if="successMessage" 
                class="alert alert-success alert-dismissible fade show" 
                role="alert"
              >
                <i class="fas fa-check-circle me-2"></i>
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
                <!-- Username Field -->
                <div class="mb-3">
                  <label for="username" class="form-label fw-semibold">
                    <i class="fas fa-user me-1"></i>
                    Username
                  </label>
                  <input 
                    type="text" 
                    class="form-control form-control-lg"
                    :class="{
                      'is-invalid': errors.username,
                      'is-valid': formData.username && !errors.username
                    }"
                    id="username"
                    v-model="formData.username"
                    placeholder="Enter your username"
                    required
                    autocomplete="username"
                    @blur="validateField('username')"
                  >
                  <div v-if="errors.username" class="invalid-feedback">
                    {{ errors.username }}
                  </div>
                </div>

                <!-- Password Field -->
                <div class="mb-3">
                  <label for="password" class="form-label fw-semibold">
                    <i class="fas fa-lock me-1"></i>
                    Password
                  </label>
                  <div class="input-group">
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="form-control form-control-lg"
                      :class="{
                        'is-invalid': errors.password,
                        'is-valid': formData.password && !errors.password
                      }"
                      id="password"
                      v-model="formData.password"
                      placeholder="Enter your password"
                      required
                      autocomplete="current-password"
                      @blur="validateField('password')"
                    >
                    <button 
                      class="btn btn-outline-secondary" 
                      type="button"
                      @click="togglePasswordVisibility"
                      tabindex="-1"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <div v-if="errors.password" class="invalid-feedback d-block">
                    {{ errors.password }}
                  </div>
                </div>

                <!-- Remember Me Checkbox -->
                <div class="mb-4 form-check">
                  <input 
                    type="checkbox" 
                    class="form-check-input" 
                    id="rememberMe"
                    v-model="formData.remember_me"
                  >
                  <label class="form-check-label" for="rememberMe">
                    Keep me signed in
                  </label>
                </div>

                <!-- Submit Button -->
                <div class="d-grid">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <i v-else class="fas fa-sign-in-alt me-2"></i>
                    {{ isLoading ? 'Signing In...' : 'Sign In' }}
                  </button>
                </div>
              </form>

              <!-- Footer -->
              <div class="text-center mt-4">
                <p class="text-muted mb-2">Don't have an account?</p>
                <router-link to="/register" class="btn btn-outline-primary">
                  <i class="fas fa-user-plus me-1"></i>
                  Create Account
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Form data matching your expected output
const formData = reactive({
  username: '',
  password: '',
  remember_me: false
})

// Form state
const isLoading = ref(false)
const showPassword = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const errors = reactive({})

// Validation rules
const validateField = (field) => {
  switch (field) {
    case 'username':
      if (!formData.username) {
        errors.username = 'Username is required'
      } else if (formData.username.length < 3) {
        errors.username = 'Username must be at least 3 characters'
      } else {
        delete errors.username
      }
      break
    
    case 'password':
      if (!formData.password) {
        errors.password = 'Password is required'
      } else if (formData.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
      } else {
        delete errors.password
      }
      break
  }
}

// Validate all fields
const validateForm = () => {
  validateField('username')
  validateField('password')
  return Object.keys(errors).length === 0
}

// Toggle password visibility
const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// Handle form submission
const handleLogin = async () => {
  if (!validateForm()) {
    errorMessage.value = 'Please fix the errors above'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  
  try {
    // Your expected output format
    const loginData = {
      username: formData.username,
      password: formData.password,
      remember_me: formData.remember_me
    }
    
    console.log('Login Data:', loginData) // This matches your expected output
    
    // Call your auth store login method
    await authStore.login(loginData)
    
    successMessage.value = 'Login successful! Redirecting...'
    
    // Redirect based on user role
    setTimeout(() => {
      if (authStore.user?.role === 'admin') {
        router.push('/admin/dashboard')
      } else {
        router.push('/dashboard')
      }
    }, 1000)
    
  } catch (error) {
    errorMessage.value = error.message || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.card {
  border-radius: 1rem;
}

.form-control:focus {
  border-color: var(--bs-primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
}

.btn-primary {
  background: linear-gradient(45deg, var(--bs-primary), #0056b3);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(var(--bs-primary-rgb), 0.3);
}

@media (max-width: 576px) {
  .card-body {
    padding: 2rem !important;
  }
}
</style>
