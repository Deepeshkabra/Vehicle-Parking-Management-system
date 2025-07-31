import { defineStore } from 'pinia'
import axios from 'axios'

// Configure axios base URL
axios.defaults.baseURL = 'http://localhost:5000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Store user object directly, not as string
    user: null,
    access_token: null,
    refresh_token: null,
    loading: false,
    error: null,
    isAuthenticated: false
  }),

  getters: {
    getUser: (state) => state.user,
    getAccessToken: (state) => state.access_token,
    getRefreshToken: (state) => state.refresh_token,
    isLoggedIn: (state) => !!state.access_token && !!state.user,
    getError: (state) => state.error,
    isLoading: (state) => state.loading
  },

  actions: {
    // Initialize auth state on app load
    initializeAuth() {
      try {
        const access_token = localStorage.getItem('access_token')
        const refresh_token = localStorage.getItem('refresh_token')
        const userStr = localStorage.getItem('user')
        
        if (access_token && refresh_token && userStr) {
          const user = JSON.parse(userStr)
          this.access_token = access_token
          this.refresh_token = refresh_token
          this.user = user
          this.isAuthenticated = true
          
          // Set axios default header
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        }
      } catch (error) {
        console.error('Error initializing auth state:', error)
        this.logout() // Clear potentially corrupted state
      }
    },

    // Login action
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/login', {
          username: credentials.username,
          password: credentials.password,
          remember_me: credentials.remember_me
        })

        const { message, data } = response.data
        
        if (message && data) {
          // Store tokens and user data in state
          this.access_token = data.access_token
          this.refresh_token = data.refresh_token
          this.user = data.user
          this.isAuthenticated = true
          
          // Store in localStorage
          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('refresh_token', data.refresh_token)
          localStorage.setItem('user', JSON.stringify(data.user))
          
          // Set axios default header
          axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
        }
        
        this.loading = false
        return Promise.resolve({ message, data })
        
      } catch (error) {
        this.loading = false
        this.error = error.response?.data?.message || 'Login failed. Please try again.'
        return Promise.reject(error)
      }
    },

    // Register action
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/register', {
          username: userData.username,
          email: userData.email,
          password: userData.password,
          confirm_password: userData.confirmPassword,
          phone: userData.phone
        })

        const { success, message } = response.data
        this.loading = false
        return Promise.resolve({ success, message })
        
      } catch (error) {
        this.loading = false
        this.error = error.response?.data?.message || 'Registration failed. Please try again.'
        return Promise.reject(error)
      }
    },

    // Logout action
    logout() {
      // Clear state
      this.user = null
      this.access_token = null
      this.refresh_token = null
      this.isAuthenticated = false
      this.error = null
      
      // Clear localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      
      // Remove axios default header
      delete axios.defaults.headers.common['Authorization']
    },

    // Clear error
    clearError() {
      this.error = null
    }
  }
})  