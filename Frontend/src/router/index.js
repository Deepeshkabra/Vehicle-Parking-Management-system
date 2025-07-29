import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
,
    {
      path: '/login',
      name: 'login',
      component: () => import('../components/auth/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../components/auth/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    // Protected routes (add these later)
    {
      path: '/admin',
      name: 'admin',
      redirect: '/admin/dashboard',
      meta: { requiresAuth: true, requiresRole: 'admin' }
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('@/views/admin/Dashboard.vue'),
      meta: { requiresAuth: true, requiresRole: 'admin' }
    },
    // {
    //   path: '/admin/parking-lots',
    //   name: 'admin-parking-lots',
    //   component: () => import('@/views/admin/ParkingLots.vue'),
    //   meta: { requiresAuth: true, requiresRole: 'admin' }
    // },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: () => import('@/views/admin/Users.vue'),
      meta: { requiresAuth: true, requiresRole: 'admin' }
    },
    // {
    //   path: '/user',
    //   name: 'user',
    //   redirect: '/user/dashboard',
    //   meta: { requiresAuth: true, requiresRole: 'user' }
    // },
    // {
    //   path: '/user/dashboard',
    //   name: 'user-dashboard',
    //   component: () => import('../views/user/Dashboard.vue'),
    //   meta: { requiresAuth: true, requiresRole: 'user' }
    // }
  ],
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth state
  authStore.initializeAuth()
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // Check if route requires guest (redirect authenticated users)
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    if (authStore.user?.role === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/user/dashboard')
    }
    return
  }
  
  // Check role-based access
  if (to.meta.requiresRole && authStore.user?.role !== to.meta.requiresRole) {
    // Redirect to appropriate dashboard based on role
    if (authStore.user?.role === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/user/dashboard')
    }
    return
  }
  
  next()
})

export default router
