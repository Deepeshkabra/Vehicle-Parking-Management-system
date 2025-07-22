import { createRouter, createWebHistory } from 'vue-router'
import { setupNavigationGuards } from './guards'
import LandingPage from '../views/LandingPage.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Public routes
    {
      path: '/',
      name: 'landing',
      component: LandingPage,
      meta: {
        title: 'Vehicle Parking Management System'
      }
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: {
        title: 'Home'
      }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: {
        title: 'About Us'
      }
    },

    // Authentication routes (guest only)
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        requiresGuest: true,
        title: 'Sign In',
        redirectIfAuthenticated: '/dashboard'
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: {
        requiresGuest: true,
        title: 'Create Account',
        redirectIfAuthenticated: '/dashboard'
      }
    },

    // Protected routes (authentication required)
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        title: 'Dashboard'
      }
    },

    // Admin routes (admin role required) - using dashboard as placeholder
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: 'Admin Panel'
      }
    },

    // User routes (user role required) - using dashboard as placeholder
    {
      path: '/bookings',
      name: 'user-bookings',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        requiresUser: true,
        title: 'My Bookings'
      }
    },
    {
      path: '/parking-lots',
      name: 'user-parking-lots',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        requiresUser: true,
        title: 'Available Parking Lots'
      }
    },

    // Shared authenticated routes - using dashboard as placeholder
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        title: 'My Profile'
      }
    },

    // Catch-all route (must be last)
    {
      path: '/:pathMatch(.*)*',
      redirect: '/not-found'
    }
  ],
})

// Setup navigation guards
setupNavigationGuards(router);

// Global after each hook for page titles
router.afterEach((to) => {
  // Update page title
  if (to.meta?.title) {
    document.title = `${to.meta.title} | ParkingManager`;
  } else {
    document.title = 'ParkingManager';
  }
});

export default router
