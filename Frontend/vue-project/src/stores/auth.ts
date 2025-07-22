import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import authService, { 
  type User, 
  type LoginCredentials, 
  type RegisterCredentials 
} from '@/services/authService';

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => !!user.value && authService.isAuthenticated());
  const isAdmin = computed(() => user.value?.role === 'admin');
  const isUser = computed(() => user.value?.role === 'user');
  const userRole = computed(() => user.value?.role || null);
  const userName = computed(() => user.value?.username || '');
  const userEmail = computed(() => user.value?.email || '');

  // Actions
  const login = async (credentials: LoginCredentials): Promise<void> => {
    try {
      isLoading.value = true;
      error.value = null;

      const response = await authService.login(credentials);
      
      if (response.success && response.data) {
        user.value = response.data.user;
      } else {
        throw new Error(response.message || 'Login failed');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      error.value = errorMessage;
      throw new Error(errorMessage);
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (credentials: RegisterCredentials): Promise<void> => {
    try {
      isLoading.value = true;
      error.value = null;

      const response = await authService.register(credentials);
      
      if (response.success && response.data) {
        user.value = response.data.user;
      } else {
        throw new Error(response.message || 'Registration failed');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Registration failed';
      error.value = errorMessage;
      throw new Error(errorMessage);
    } finally {
      isLoading.value = false;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      isLoading.value = true;
      error.value = null;

      await authService.logout();
      
      // Clear user state
      user.value = null;
    } catch (err) {
      // Even if logout API fails, clear local state
      console.error('Logout error:', err);
      user.value = null;
    } finally {
      isLoading.value = false;
    }
  };

  const refreshToken = async (): Promise<void> => {
    try {
      const response = await authService.refreshToken();
      
      if (response.success && response.data) {
        user.value = response.data.user;
      } else {
        throw new Error(response.message || 'Token refresh failed');
      }
    } catch (err) {
      console.error('Token refresh failed:', err);
      // Clear user state on refresh failure
      user.value = null;
      authService.clearTokens();
      throw err;
    }
  };

  const checkAuth = async (): Promise<void> => {
    try {
      if (!authService.isAuthenticated()) {
        user.value = null;
        return;
      }

      isLoading.value = true;
      
      const currentUser = await authService.getCurrentUser();
      
      if (currentUser) {
        user.value = currentUser;
      } else {
        // If can't get user info, clear auth state
        user.value = null;
        authService.clearTokens();
      }
    } catch (err) {
      console.error('Auth check failed:', err);
      user.value = null;
      authService.clearTokens();
    } finally {
      isLoading.value = false;
    }
  };

  const clearError = (): void => {
    error.value = null;
  };

  const setUser = (userData: User): void => {
    user.value = userData;
  };

  const clearUser = (): void => {
    user.value = null;
    authService.clearTokens();
  };

  // Initialize auth state on store creation
  const initialize = async (): Promise<void> => {
    if (authService.isAuthenticated()) {
      await checkAuth();
    }
  };

  // Validation helpers
  const validateLoginForm = (credentials: Partial<LoginCredentials>): string[] => {
    const errors: string[] = [];

    if (!credentials.username?.trim()) {
      errors.push('Username or email is required');
    }

    if (!credentials.password?.trim()) {
      errors.push('Password is required');
    }

    return errors;
  };

  const validateRegisterForm = (credentials: Partial<RegisterCredentials>): string[] => {
    const errors: string[] = [];

    // Username validation
    if (!credentials.username?.trim()) {
      errors.push('Username is required');
    } else {
      const usernameValidation = authService.validateUsername(credentials.username);
      if (!usernameValidation.isValid) {
        errors.push(...usernameValidation.errors);
      }
    }

    // Email validation
    if (!credentials.email?.trim()) {
      errors.push('Email is required');
    } else if (!authService.validateEmail(credentials.email)) {
      errors.push('Please enter a valid email address');
    }

    // Password validation
    if (!credentials.password?.trim()) {
      errors.push('Password is required');
    } else {
      const passwordValidation = authService.validatePassword(credentials.password);
      if (!passwordValidation.isValid) {
        errors.push(...passwordValidation.errors);
      }
    }

    return errors;
  };

  const getPasswordStrength = (password: string) => {
    return authService.validatePassword(password);
  };

  // Auto-refresh token before expiry
  const startTokenRefreshTimer = (): void => {
    // Refresh token every 14 minutes (assuming 15-minute token expiry)
    const refreshInterval = 14 * 60 * 1000; // 14 minutes in milliseconds
    
    const refreshTimer = setInterval(async () => {
      if (isAuthenticated.value) {
        try {
          await refreshToken();
        } catch (error) {
          console.error('Auto token refresh failed:', error);
          clearInterval(refreshTimer);
        }
      } else {
        clearInterval(refreshTimer);
      }
    }, refreshInterval);
  };

  return {
    // State
    user,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    isAdmin,
    isUser,
    userRole,
    userName,
    userEmail,
    
    // Actions
    login,
    register,
    logout,
    refreshToken,
    checkAuth,
    clearError,
    setUser,
    clearUser,
    initialize,
    
    // Validation helpers
    validateLoginForm,
    validateRegisterForm,
    getPasswordStrength,
    
    // Token management
    startTokenRefreshTimer
  };
});

// Export the store
export default useAuthStore; 