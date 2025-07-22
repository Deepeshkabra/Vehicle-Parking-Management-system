import apiClient, { type ApiResponse, handleApiError, tokenManager } from './apiClient';

// Type definitions
export interface LoginCredentials {
  username: string;
  password: string;
  remember_me?: boolean;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
  phone?: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: 'admin' | 'user';
  is_active: boolean;
  created_at: string | null;
  last_login: string;
  phone: string | null;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data?: {
    access_token: string;
    refresh_token: string;
    user: User;
  };
  errors?: any;
}

export interface AuthError {
  message: string;
  errors?: any;
  status?: number;
}

class AuthService {
  /**
   * Login user or admin
   * @param credentials Login credentials
   * @returns Promise with authentication response
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<ApiResponse<{
        access_token: string;
        refresh_token: string;
        user: User;
      }>>('/api/auth/login', credentials);

      if (response.data.success && response.data.data) {
        // Store tokens
        this.setTokens(
          response.data.data.access_token,
          response.data.data.refresh_token
        );

        return {
          success: true,
          message: response.data.message,
          data: response.data.data
        };
      }

      return {
        success: false,
        message: response.data.message || 'Login failed',
        errors: response.data.errors
      };
    } catch (error) {
      const apiError = handleApiError(error);
      throw new Error(apiError.message);
    }
  }

  /**
   * Register new user (not for admin)
   * @param credentials Registration credentials
   * @returns Promise with authentication response
   */
  async register(credentials: RegisterCredentials): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<ApiResponse<{
        access_token: string;
        refresh_token: string;
        user: User;
      }>>('/api/auth/register', credentials);

      if (response.data.success && response.data.data) {
        // Store tokens
        this.setTokens(
          response.data.data.access_token,
          response.data.data.refresh_token
        );

        return {
          success: true,
          message: response.data.message,
          data: response.data.data
        };
      }

      return {
        success: false,
        message: response.data.message || 'Registration failed',
        errors: response.data.errors
      };
    } catch (error) {
      const apiError = handleApiError(error);
      return {
        success: false,
        message: apiError.message,
        errors: apiError.errors
      };
    }
  }

  /**
   * Logout current user
   * @returns Promise<void>
   */
  async logout(): Promise<void> {
    try {
      // Call logout endpoint to blacklist token
      await apiClient.post('/api/auth/logout');
    } catch (error) {
      // Continue with logout even if API call fails
      console.error('Logout API call failed:', error);
    } finally {
      // Always clear local tokens
      this.clearTokens();
    }
  }

  /**
   * Refresh access token using refresh token
   * @returns Promise with new access token
   */
  async refreshToken(): Promise<AuthResponse> {
    try {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await apiClient.post<ApiResponse<{
        access_token: string;
        user: User;
      }>>('/api/auth/refresh', {}, {
        headers: {
          Authorization: `Bearer ${refreshToken}`
        }
      });

      if (response.data.success && response.data.data) {
        // Update access token, keep existing refresh token
        const currentRefreshToken = this.getRefreshToken();
        if (currentRefreshToken) {
          this.setTokens(response.data.data.access_token, currentRefreshToken);
        }

        return {
          success: true,
          message: response.data.message,
          data: {
            access_token: response.data.data.access_token,
            refresh_token: currentRefreshToken!,
            user: response.data.data.user
          }
        };
      }

      throw new Error(response.data.message || 'Token refresh failed');
    } catch (error) {
      const apiError = handleApiError(error);
      // Clear tokens on refresh failure
      this.clearTokens();
      throw new Error(apiError.message);
    }
  }

  /**
   * Get current user information
   * @returns Promise with current user data
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      const response = await apiClient.get<ApiResponse<{ user: User }>>('/api/auth/me');

      if (response.data.success && response.data.data) {
        return response.data.data.user;
      }

      return null;
    } catch (error) {
      console.error('Get current user failed:', error);
      return null;
    }
  }

  /**
   * Store access and refresh tokens
   * @param accessToken JWT access token
   * @param refreshToken JWT refresh token
   */
  setTokens(accessToken: string, refreshToken: string): void {
    tokenManager.setTokens(accessToken, refreshToken);
  }

  /**
   * Get stored access token
   * @returns Access token or null
   */
  getAccessToken(): string | null {
    return tokenManager.getAccessToken();
  }

  /**
   * Get stored refresh token
   * @returns Refresh token or null
   */
  getRefreshToken(): string | null {
    return tokenManager.getRefreshToken();
  }

  /**
   * Clear all stored tokens
   */
  clearTokens(): void {
    tokenManager.clearTokens();
  }

  /**
   * Check if user is authenticated
   * @returns Boolean indicating authentication status
   */
  isAuthenticated(): boolean {
    const accessToken = this.getAccessToken();
    return !!accessToken;
  }

  /**
   * Get current user role from stored token
   * @returns User role or null
   */
  getCurrentUserRole(): 'admin' | 'user' | null {
    const accessToken = this.getAccessToken();
    if (!accessToken) return null;

    try {
      // Decode JWT payload (basic parsing without verification)
      const base64Url = accessToken.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      const payload = JSON.parse(jsonPayload);
      return payload.role || null;
    } catch (error) {
      console.error('Failed to decode token:', error);
      return null;
    }
  }

  /**
   * Check if current user is admin
   * @returns Boolean indicating admin status
   */
  isAdmin(): boolean {
    return this.getCurrentUserRole() === 'admin';
  }

  /**
   * Check if current user is regular user
   * @returns Boolean indicating user status
   */
  isUser(): boolean {
    return this.getCurrentUserRole() === 'user';
  }

  /**
   * Validate email format
   * @param email Email to validate
   * @returns Boolean indicating valid email
   */
  validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Validate password strength
   * @param password Password to validate
   * @returns Object with validation result and feedback
   */
  validatePassword(password: string): {
    isValid: boolean;
    errors: string[];
    strength: 'weak' | 'medium' | 'strong';
  } {
    const errors: string[] = [];
    let score = 0;

    // Length check
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    } else {
      score += 1;
    }

    // Uppercase check
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    } else {
      score += 1;
    }

    // Lowercase check
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    } else {
      score += 1;
    }

    // Number check
    if (!/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    } else {
      score += 1;
    }

    // Special character check
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push('Password must contain at least one special character');
    } else {
      score += 1;
    }

    // Determine strength
    let strength: 'weak' | 'medium' | 'strong' = 'weak';
    if (score >= 4) strength = 'strong';
    else if (score >= 3) strength = 'medium';

    return {
      isValid: errors.length === 0,
      errors,
      strength
    };
  }

  /**
   * Validate username format
   * @param username Username to validate
   * @returns Object with validation result
   */
  validateUsername(username: string): {
    isValid: boolean;
    errors: string[];
  } {
    const errors: string[] = [];

    // Length check
    if (username.length < 3 || username.length > 20) {
      errors.push('Username must be between 3 and 20 characters');
    }

    // Alphanumeric check
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      errors.push('Username can only contain letters, numbers, and underscores');
    }

    // Must start with letter
    if (!/^[a-zA-Z]/.test(username)) {
      errors.push('Username must start with a letter');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

// Export singleton instance
export const authService = new AuthService();
export default authService; 