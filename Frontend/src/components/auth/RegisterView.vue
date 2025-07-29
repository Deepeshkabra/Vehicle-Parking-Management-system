<template>
  <div class="min-vh-100 d-flex align-items-center bg-light py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <i class="fas fa-user-plus text-primary mb-3" style="font-size: 3rem;"></i>
                <h2 class="card-title fw-bold text-dark">Create Account</h2>
                <p class="text-muted">Join ParkEase today</p>
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

              <!-- Registration Form -->
              <form @submit.prevent="handleRegister" novalidate>
                <!-- Username Field -->
                <div class="mb-3">
                  <label for="regUsername" class="form-label fw-semibold">
                    <i class="fas fa-user me-1"></i>
                    Username *
                  </label>
                  <input 
                    type="text" 
                    class="form-control"
                    :class="{
                      'is-invalid': errors.username,
                      'is-valid': formData.username && !errors.username
                    }"
                    id="regUsername"
                    v-model="formData.username"
                    placeholder="Choose a unique username"
                    required
                    autocomplete="username"
                    @blur="validateField('username')"
                    @input="validateField('username')"
                  >
                  <div v-if="errors.username" class="invalid-feedback">
                    {{ errors.username }}
                  </div>
                  <div v-else class="form-text">
                    Username must be 3-20 characters long
                  </div>
                </div>

                <!-- Email Field -->
                <div class="mb-3">
                  <label for="email" class="form-label fw-semibold">
                    <i class="fas fa-envelope me-1"></i>
                    Email Address *
                  </label>
                  <input 
                    type="email" 
                    class="form-control"
                    :class="{
                      'is-invalid': errors.email,
                      'is-valid': formData.email && !errors.email
                    }"
                    id="email"
                    v-model="formData.email"
                    placeholder="your.email@example.com"
                    required
                    autocomplete="email"
                    @blur="validateField('email')"
                  >
                  <div v-if="errors.email" class="invalid-feedback">
                    {{ errors.email }}
                  </div>
                </div>

                <!-- Phone Field -->
                <div class="mb-3">
                  <label for="phone" class="form-label fw-semibold">
                    <i class="fas fa-phone me-1"></i>
                    Phone Number *
                  </label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-phone"></i>
                    </span>
                    <input 
                      type="tel" 
                      class="form-control"
                      :class="{
                        'is-invalid': errors.phone,
                        'is-valid': formData.phone && !errors.phone
                      }"
                      id="phone"
                      v-model="formData.phone"
                      placeholder="+1234567890"
                      required
                      autocomplete="tel"
                      @blur="validateField('phone')"
                    >
                  </div>
                  <div v-if="errors.phone" class="invalid-feedback d-block">
                    {{ errors.phone }}
                  </div>
                  <div v-else class="form-text">
                    Include country code (e.g., +1234567890)
                  </div>
                </div>

                <!-- Password Field -->
                <div class="mb-3">
                  <label for="regPassword" class="form-label fw-semibold">
                    <i class="fas fa-lock me-1"></i>
                    Password *
                  </label>
                  <div class="input-group">
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="form-control"
                      :class="{
                        'is-invalid': errors.password,
                        'is-valid': formData.password && !errors.password
                      }"
                      id="regPassword"
                      v-model="formData.password"
                      placeholder="Create a strong password"
                      required
                      autocomplete="new-password"
                      @blur="validateField('password')"
                      @input="validateField('password')"
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
                  
                  <!-- Password Strength Indicator -->
                  <div v-if="formData.password" class="mt-2">
                    <div class="progress" style="height: 5px;">
                      <div 
                        class="progress-bar"
                        :class="passwordStrengthClass"
                        :style="{ width: passwordStrengthWidth }"
                      ></div>
                    </div>
                    <small class="text-muted">{{ passwordStrengthText }}</small>
                  </div>
                </div>

                <!-- Confirm Password Field -->
                <div class="mb-3">
                  <label for="confirmPassword" class="form-label fw-semibold">
                    <i class="fas fa-lock me-1"></i>
                    Confirm Password *
                  </label>
                  <input 
                    type="password" 
                    class="form-control"
                    :class="{
                      'is-invalid': errors.confirmPassword,
                      'is-valid': confirmPassword && !errors.confirmPassword
                    }"
                    id="confirmPassword"
                    v-model="confirmPassword"
                    placeholder="Repeat your password"
                    required
                    autocomplete="new-password"
                    @blur="validateField('confirmPassword')"
                  >
                  <div v-if="errors.confirmPassword" class="invalid-feedback">
                    {{ errors.confirmPassword }}
                  </div>
                </div>

                <!-- Terms and Conditions -->
                <div class="mb-4 form-check">
                  <input 
                    type="checkbox" 
                    class="form-check-input"
                    :class="{ 'is-invalid': errors.terms }"
                    id="termsCheck"
                    v-model="agreeToTerms"
                    required
                    @change="validateField('terms')"
                  >
                  <label class="form-check-label" for="termsCheck">
                    I agree to the 
                    <a href="#" class="text-primary text-decoration-none" @click.prevent="showTerms = true">
                      Terms of Service
                    </a> 
                    and 
                    <a href="#" class="text-primary text-decoration-none" @click.prevent="showPrivacy = true">
                      Privacy Policy
                    </a>
                  </label>
                  <div v-if="errors.terms" class="invalid-feedback d-block">
                    {{ errors.terms }}
                  </div>
                </div>

                <!-- Submit Button -->
                <div class="d-grid">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg"
                    :disabled="isLoading || !isFormValid"
                  >
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <i v-else class="fas fa-user-plus me-2"></i>
                    {{ isLoading ? 'Creating Account...' : 'Create Account' }}
                  </button>
                </div>
              </form>

              <!-- Footer -->
              <div class="text-center mt-4">
                <p class="text-muted mb-2">Already have an account?</p>
                <router-link to="/login" class="btn btn-outline-primary">
                  <i class="fas fa-sign-in-alt me-1"></i>
                  Sign In
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
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Form data matching your expected output
const formData = reactive({
  username: '',
  email: '',
  password: '',
  phone: ''
})

// Additional form state
const confirmPassword = ref('')
const agreeToTerms = ref(false)
const isLoading = ref(false)
const showPassword = ref(false)
const errorMessage = ref('')
const errors = reactive({})

// Password strength calculation
const passwordStrength = computed(() => {
  const password = formData.password
  let strength = 0
  
  if (password.length >= 8) strength += 1
  if (/[A-Z]/.test(password)) strength += 1
  if (/[a-z]/.test(password)) strength += 1
  if (/[0-9]/.test(password)) strength += 1
  if (/[^A-Za-z0-9]/.test(password)) strength += 1
  
  return strength
})

const passwordStrengthClass = computed(() => {
  switch (passwordStrength.value) {
    case 1: return 'bg-danger'
    case 2: return 'bg-warning'
    case 3: return 'bg-info'
    case 4: return 'bg-success'
    case 5: return 'bg-primary'
    default: return 'bg-light'
  }
})

const passwordStrengthWidth = computed(() => `${passwordStrength.value * 20}%`)

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 1: return 'Very Weak'
    case 2: return 'Weak'
    case 3: return 'Fair'
    case 4: return 'Good'
    case 5: return 'Strong'
    default: return ''
  }
})

const isFormValid = computed(() => {
  return Object.keys(errors).length === 0 && 
         formData.username && 
         formData.email && 
         formData.password && 
         formData.phone &&
         confirmPassword.value &&
         agreeToTerms.value
})

// Validation functions
const validateField = (field) => {
  switch (field) {
    case 'username':
      if (!formData.username) {
        errors.username = 'Username is required'
      } else if (formData.username.length < 3) {
        errors.username = 'Username must be at least 3 characters'
      } else if (formData.username.length > 20) {
        errors.username = 'Username must be less than 20 characters'
      } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
        errors.username = 'Username can only contain letters, numbers, and underscores'
      } else {
        delete errors.username
      }
      break
    
    case 'email':
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!formData.email) {
        errors.email = 'Email is required'
      } else if (!emailRegex.test(formData.email)) {
        errors.email = 'Please enter a valid email address'
      } else {
        delete errors.email
      }
      break
    
    case 'phone':
      const phoneRegex = /^\+[1-9]\d{1,14}$/
      if (!formData.phone) {
        errors.phone = 'Phone number is required'
      } else if (!phoneRegex.test(formData.phone)) {
        errors.phone = 'Please enter a valid phone number with country code (e.g., +1234567890)'
      } else {
        delete errors.phone
      }
      break
    
    case 'password':
      if (!formData.password) {
        errors.password = 'Password is required'
      } else if (formData.password.length < 8) {
        errors.password = 'Password must be at least 8 characters'
      } else if (passwordStrength.value < 3) {
        errors.password = 'Password is too weak. Use uppercase, lowercase, numbers, and symbols'
      } else {
        delete errors.password
      }
      break
    
    case 'confirmPassword':
      if (!confirmPassword.value) {
        errors.confirmPassword = 'Please confirm your password'
      } else if (confirmPassword.value !== formData.password) {
        errors.confirmPassword = 'Passwords do not match'
      } else {
        delete errors.confirmPassword
      }
      break
    
    case 'terms':
      if (!agreeToTerms.value) {
        errors.terms = 'You must agree to the terms and conditions'
      } else {
        delete errors.terms
      }
      break
  }
}

const validateForm = () => {
  validateField('username')
  validateField('email')
  validateField('phone')
  validateField('password')
  validateField('confirmPassword')
  validateField('terms')
  return Object.keys(errors).length === 0
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleRegister = async () => {
  if (!validateForm()) {
    errorMessage.value = 'Please fix the errors above'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  
  try {
    // Your expected output format
    const registerData = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      phone: formData.phone
    }
    
    console.log('Register Data:', registerData) // This matches your expected output
    
    // Call your auth store register method
    await authStore.register(registerData)
    
    // Redirect to login with success message
    router.push({
      path: '/login',
      query: { message: 'Registration successful! Please sign in.' }
    })
    
  } catch (error) {
    errorMessage.value = error.message || 'Registration failed. Please try again.'
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

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(var(--bs-primary-rgb), 0.3);
}

.progress {
  transition: all 0.3s ease;
}

@media (max-width: 576px) {
  .card-body {
    padding: 2rem !important;
  }
}
</style>
