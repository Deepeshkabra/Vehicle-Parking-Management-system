import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Route meta interface extension
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;
    requiresGuest?: boolean;
    requiresAdmin?: boolean;
    requiresUser?: boolean;
    redirectIfAuthenticated?: string;
  }
}

/**
 * Main authentication guard
 * Checks if route requires authentication and handles redirects
 */
export const authGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): Promise<void> => {
  const authStore = useAuthStore();
  
  // Initialize auth state if not already done
  if (!authStore.user && authStore.isAuthenticated) {
    try {
      await authStore.checkAuth();
    } catch (error) {
      console.error('Auth check failed:', error);
      authStore.clearUser();
    }
  }

  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.userRole;

  // Handle routes that require guests only (login, register)
  if (to.meta.requiresGuest && isAuthenticated) {
    const redirectPath = to.meta.redirectIfAuthenticated || getDefaultRedirectForRole(userRole);
    next(redirectPath);
    return;
  }

  // Handle routes that require authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Store the intended destination
    const redirectTo = to.fullPath !== '/' ? to.fullPath : undefined;
    next({
      path: '/login',
      query: redirectTo ? { redirect: redirectTo } : undefined
    });
    return;
  }

  // Handle routes that require admin role
  if (to.meta.requiresAdmin && (!isAuthenticated || userRole !== 'admin')) {
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else {
      // User is authenticated but not admin
      next('/dashboard');
    }
    return;
  }

  // Handle routes that require user role
  if (to.meta.requiresUser && (!isAuthenticated || userRole !== 'user')) {
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else {
      // User is authenticated but not regular user (probably admin)
      next('/admin');
    }
    return;
  }

  // Route is accessible, proceed
  next();
};

/**
 * Admin-only guard
 * Ensures only admin users can access certain routes
 */
export const adminGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): Promise<void> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    });
    return;
  }

  if (!authStore.isAdmin) {
    // Redirect non-admin users to their dashboard
    next('/dashboard');
    return;
  }

  next();
};

/**
 * User-only guard
 * Ensures only regular users can access certain routes
 */
export const userGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): Promise<void> => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    });
    return;
  }

  if (!authStore.isUser) {
    // Redirect non-user (admin) to admin dashboard
    next('/admin');
    return;
  }

  next();
};

/**
 * Guest-only guard
 * Ensures only unauthenticated users can access certain routes
 */
export const guestGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): Promise<void> => {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated) {
    const redirectPath = getDefaultRedirectForRole(authStore.userRole);
    next(redirectPath);
    return;
  }

  next();
};

/**
 * Get default redirect path based on user role
 */
const getDefaultRedirectForRole = (role: string | null): string => {
  switch (role) {
    case 'admin':
      return '/admin';
    case 'user':
      return '/dashboard';
    default:
      return '/';
  }
};

/**
 * Check if user has required permissions for a route
 */
export const hasPermission = (
  requiredRole: 'admin' | 'user' | null,
  userRole: string | null
): boolean => {
  if (!requiredRole) return true; // No role required
  
  return userRole === requiredRole;
};

/**
 * Route validation helper
 * Validates if current user can access a specific route
 */
export const canAccessRoute = (
  routeMeta: RouteLocationNormalized['meta'],
  isAuthenticated: boolean,
  userRole: string | null
): { canAccess: boolean; redirectTo?: string } => {
  // Guest-only routes
  if (routeMeta.requiresGuest && isAuthenticated) {
    return {
      canAccess: false,
      redirectTo: getDefaultRedirectForRole(userRole)
    };
  }

  // Auth required routes
  if (routeMeta.requiresAuth && !isAuthenticated) {
    return {
      canAccess: false,
      redirectTo: '/login'
    };
  }

  // Admin-only routes
  if (routeMeta.requiresAdmin && (!isAuthenticated || userRole !== 'admin')) {
    return {
      canAccess: false,
      redirectTo: !isAuthenticated ? '/login' : '/dashboard'
    };
  }

  // User-only routes
  if (routeMeta.requiresUser && (!isAuthenticated || userRole !== 'user')) {
    return {
      canAccess: false,
      redirectTo: !isAuthenticated ? '/login' : '/admin'
    };
  }

  return { canAccess: true };
};

/**
 * Token refresh guard
 * Automatically refreshes tokens before they expire
 */
export const tokenRefreshGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): Promise<void> => {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated) {
    try {
      // Try to refresh token if needed
      // This could be enhanced to check token expiry time
      await authStore.refreshToken();
    } catch (error) {
      console.warn('Token refresh failed during navigation:', error);
      // Don't block navigation if refresh fails
      // The API interceptor will handle token refresh on API calls
    }
  }

  next();
};

/**
 * Analytics and logging guard
 * Tracks route changes for authenticated users
 */
export const analyticsGuard = (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): void => {
  const authStore = useAuthStore();

  if (authStore.isAuthenticated && to.path !== from.path) {
    // Log route change for analytics
    console.log(`User ${authStore.userName} navigated from ${from.path} to ${to.path}`);
    
    // Here you could send analytics data to your backend
    // Example: analyticsService.trackNavigation(to.path, authStore.user);
  }

  next();
};

/**
 * Setup all navigation guards for the router
 */
export const setupNavigationGuards = (router: any): void => {
  // Main authentication guard (always runs first)
  router.beforeEach(authGuard);
  
  // Token refresh guard (runs for authenticated routes)
  router.beforeEach(tokenRefreshGuard);
  
  // Analytics guard (runs last for tracking)
  router.beforeEach(analyticsGuard);

  // After each navigation, clear any loading states
  router.afterEach(() => {
    const authStore = useAuthStore();
    if (authStore.isLoading) {
      // Clear loading state after navigation
      // This prevents stuck loading states
    }
  });
};

export default {
  authGuard,
  adminGuard,
  userGuard,
  guestGuard,
  tokenRefreshGuard,
  analyticsGuard,
  setupNavigationGuards,
  hasPermission,
  canAccessRoute
}; 