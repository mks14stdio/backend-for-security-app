/**
 * Comprehensive API Service Layer
 * Handles all HTTP requests to the backend
 */

import axios from 'axios'
import api from './index'

// ============================================================================
// AUTH ENDPOINTS
// ============================================================================

export const authService = {

  login: async (email, password) => {
    try {
      const response = await api.post('/v1/login', { "email": email, "password": password })
      var json_data = response.data;
      localStorage.setItem("token", json_data.access_token);
      localStorage.setItem("refresh", json_data.refresh_token);
      return true;
    } catch (err) {
      console.error(err)
      return false;
    }
  }
}

/**
 * Decode JWT token payload (without verification)
 * Note: This only decodes, does not verify signature
 */
export const decodeToken = (token) => {
  try {
    const payload = token.split('.')[1]
    const decoded = JSON.parse(atob(payload))
    return decoded
  } catch (error) {
    console.error('Failed to decode token:', error)
    return null
  }
}

/**
 * Get stored user info from localStorage
 */
export const getStoredUser = () => {
  const userJson = localStorage.getItem('user')
  return userJson ? JSON.parse(userJson) : null
}

/**
 * Store user info in localStorage
 */
export const storeUser = (user) => {
  localStorage.setItem('user', JSON.stringify(user))
}

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return !!localStorage.getItem('token')
}

/**
 * Check if user has admin role
 */
export const isAdmin = () => {
  const user = getStoredUser()
  return user?.role === 'admin' || user?.role === 'ADMIN'
}

/**
 * Check if user has editor role
 */
export const isEditor = () => {
  const user = getStoredUser()
  return user?.role === 'editor' || user?.role === 'EDITOR' || isAdmin()
}

/**
 * Get current user role
 */
export const getUserRole = () => {
  const user = getStoredUser()
  return user?.role || 'user'
}

export const articleService = {

  create: async () => {

  },

  get_all: async (limit, offset) => {
    try {
        const response = await api.get('/v1/article/', { params: { limit: limit, offset: offset }})
        var json_data = response.data;
        return json_data;
    } catch (err) {
      console.log(err)
      return false
    }
  },

  add: async (content, test_pk) => {
    try {
      const response = await api.post('/v1/article/', { "content": content, "test_pk": test_pk })
      var json_data = response.data;
      return json_data;
    } catch (err) {
      console.error(err)
      return false;
    }
  }

}


export default {
  authService,
  decodeToken,
  storeUser
}
