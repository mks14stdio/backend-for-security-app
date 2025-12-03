import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
})

// attach token and refresh logic
let isRefreshing = false
let refreshPromise = null

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config
    if (err.response && err.response.status === 401 && !original._retry) {
      // try refresh
      original._retry = true
      if (!isRefreshing) {
        isRefreshing = true
        const refresh_token = localStorage.getItem('refresh_token')
        if (!refresh_token) {
          isRefreshing = false
          return Promise.reject(err)
        }
        refreshPromise = api.post('/v1/refresh/', { refresh_token })
          .then(r => {
            // server returns new tokens? openapi shows empty schema for refresh success; handle both
            const data = r.data || {}
            if (data.access_token) localStorage.setItem('access_token', data.access_token)
            if (data.refresh_token) localStorage.setItem('refresh_token', data.refresh_token)
            isRefreshing = false
            return r
          }).catch(e => { isRefreshing = false; throw e })
      }
      try {
        await refreshPromise
        original.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`
        return api(original)
      } catch (e) {
        // failed refresh, clear tokens
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        return Promise.reject(err)
      }
    }
    return Promise.reject(err)
  }
)

export default api