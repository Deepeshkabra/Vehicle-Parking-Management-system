import axios, { type AxiosInstance, type AxiosResponse, AxiosError } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
const TOKEN_STORAGE_KEY = 'parking_app_tokens';

// Token management utilities
export const tokenManager = {
  getTokens(): { accessToken: string | null; refreshToken: string | null } {
    const stored = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch {
        return { accessToken: null, refreshToken: null };
      }
    }
    return { accessToken: null, refreshToken: null };
  },

  setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify({ accessToken, refreshToken }));
  },

  clearTokens(): void {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  },

  getAccessToken(): string | null {
    return this.getTokens().accessToken;
  },

  getRefreshToken(): string | null {
    return this.getTokens().refreshToken;
  }
};

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Flag to prevent multiple refresh requests
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (value?: any) => void;
  reject: (reason?: any) => void;
}> = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  
  failedQueue = [];
};

// Request interceptor to add authorization header
apiClient.interceptors.request.use(
  (config: any) => {
    const accessToken = tokenManager.getAccessToken();
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If already refreshing, queue this request
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => {
          const newAccessToken = tokenManager.getAccessToken();
          if (originalRequest.headers && newAccessToken) {
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          }
          return apiClient(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = tokenManager.getRefreshToken();
      
      if (!refreshToken) {
        // No refresh token, clear tokens and redirect to login
        tokenManager.clearTokens();
        processQueue(error, null);
        isRefreshing = false;
        // Redirect to login page
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`
          }
        });

        if (response.data.success && response.data.data?.access_token) {
          const newAccessToken = response.data.data.access_token;
          const currentRefreshToken = tokenManager.getRefreshToken();
          
          // Update stored tokens
          if (currentRefreshToken) {
            tokenManager.setTokens(newAccessToken, currentRefreshToken);
          }

          // Update authorization header for the original request
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          }

          processQueue(null, newAccessToken);
          isRefreshing = false;

          // Retry the original request
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        tokenManager.clearTokens();
        processQueue(refreshError, null);
        isRefreshing = false;
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// API Response types
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  errors?: any;
}

export interface ApiError {
  message: string;
  errors?: any;
  status?: number;
}

// Enhanced error handling
export const handleApiError = (error: any): ApiError => {
  if (axios.isAxiosError(error)) {
    const response = error.response;
    
    if (response?.data) {
      return {
        message: response.data.message || 'An error occurred',
        errors: response.data.errors,
        status: response.status
      };
    }
    
    if (error.request) {
      return {
        message: 'Network error. Please check your connection.',
        status: 0
      };
    }
  }
  
  return {
    message: error.message || 'An unexpected error occurred',
    status: 500
  };
};

export default apiClient; 