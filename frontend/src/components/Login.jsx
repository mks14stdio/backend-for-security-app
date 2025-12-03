import React, { useState } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function submit(e) {
    e.preventDefault()
    try {
      const r = await api.post('/v1/login/', { email, password })
      const data = r.data
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      setError(null)
      if (onLogin) onLogin()
      navigate('/')
    } catch (e) {
      setError(e.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="card center">
      <h2>Login</h2>
      <form onSubmit={submit} className="form">
        <label>Email<input value={email} onChange={e=>setEmail(e.target.value)} type="email" required /></label>
        <label>Password<input value={password} onChange={e=>setPassword(e.target.value)} type="password" required minLength={8} /></label>
        {error && <div className="error">{JSON.stringify(error)}</div>}
        <button className="btn">Sign in</button>
      </form>
      <div className="muted">Only users with role <strong>admin</strong> or <strong>editor</strong> can access the app.</div>
    </div>
  )
}
