// api/index.js
import axios from 'axios'
import router from '@/router'

import service from './service'

const api = axios.create({
  baseURL: 'http://localhost:8000/',
  timeout: 10000
})

// Интерцептор для добавления токена
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Интерцептор для обработки ответов
api.interceptors.response.use(
  response => response,
  error => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (!refreshToken) {
        localStorage.clear();
        router.push('/login');
        return Promise.reject(error);
      }
      
      // Return a promise chain for refresh token
      return api.post('/refresh', { refresh_token: refreshToken })
        .then(response => {
          const { token, refresh_token: newRefreshToken } = response.data;
          
          // Update tokens
          localStorage.setItem('token', token);
          if (newRefreshToken) {
            localStorage.setItem('refresh_token', newRefreshToken);
          }
          
          const payload = service.decodeToken(token);
          service.storeUser(payload)

          // Update headers
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          originalRequest.headers['Authorization'] = `Bearer ${token}`;
          
          // Retry original request
          return api(originalRequest);
        })
        .catch(refreshError => {
          // Refresh failed
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
          router.push('/login');
          return Promise.reject(refreshError);
        });
    }
    
    return Promise.reject(error);
  }
);
export default api