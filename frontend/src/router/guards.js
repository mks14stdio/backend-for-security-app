/**
 * Router Guards for Authentication and Authorization
 */

import { isAuthenticated, isAdmin, isEditor, getUserRole } from '@/api/service'

/**
 * Check if user is authenticated
 * Redirect to login if not
 */
export const requireAuth = (to, from, next) => {
  if (isAuthenticated()) {
    next()
  } else {
    next('/login')
  }
}

/**
 * Check if user has admin role
 * Redirect to login if not authenticated or not admin
 */
export const requireAdmin = (to, from, next) => {
  if (!isAuthenticated()) {
    next('/login')
  } else if (isAdmin()) {
    next()
  } else {
    // User is not admin, redirect to login or home
    next('/login')
  }
}

export const requireAdminOrEditor = (to, from, next) => {
    if (!isAuthenticated()) {
    next('/login')
  } else if (isAdmin() || isEditor()) {
  } else {
    // User is not admin, redirect to login or home
    next('/login')
  }
}

/**
 * Check if user has editor role (or admin)
 * Redirect to login if not authenticated or not editor
 */
export const requireEditor = (to, from, next) => {
  if (!isAuthenticated()) {
    next('/login')
  } else if (isEditor()) {
    next()
  } else {
    next('/login')
  }
}

/**
 * Check if user is regular user (not admin)
 * Redirect if admin or not authenticated
 */
export const requireUser = (to, from, next) => {
  if (!isAuthenticated()) {
    next('/login')
  } else if (!isAdmin()) {
    next()
  } else {
    // Admin should not access user-only pages
    next('/')
  }
}

/**
 * Allow only unauthenticated users (redirect to home if already logged in)
 */
export const requireGuest = (to, from, next) => {
  if (!isAuthenticated()) {
    next()
  } else {
    next('/')
  }
}
