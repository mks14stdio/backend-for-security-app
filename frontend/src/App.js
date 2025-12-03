import React, { useEffect, useState } from 'react'
import { Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import AdminArea from './components/AdminArea'
import EditorArea from './components/EditorArea'
import NotFound from './components/NotFound'
import api from './api'

function ProtectedRoute({ children, roles }) {
  const [me, setMe] = useState(null)
  useEffect(() => {
    let mounted = true
    api.get('/v1/me/').then(r => mounted && setMe(r.data)).catch(() => mounted && setMe(false))
    return () => { mounted = false }
  }, [])

  if (me === null) return <div className="center">Loading...</div>
  if (me === false) return <Navigate to="/login" replace />
  if (roles && !roles.includes(me.role)) return <div className="center">Access denied. Your role: {me.role}</div>
  return children
}

export default function App() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)

  useEffect(() => {
    api.get('/v1/me/').then(r => { setUser(r.data) }).catch(() => setUser(null))
  }, [])

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    navigate('/login')
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">AdminEditorApp</div>
        <nav>
          {user ? (
            <>
              <Link to="/">Dashboard</Link>
              {user.role === 'admin' && <Link to="/admin">Users</Link>}
              {(user.role === 'editor' || user.role === 'admin') && <Link to="/editor">Content</Link>}
              <button className="btn small" onClick={logout}>Logout</button>
            </>
          ) : (
            <Link to="/login">Login</Link>
          )}
        </nav>
      </header>

      <main className="container">
        <Routes>
          <Route path="/login" element={<Login onLogin={() => window.location.reload()} />} />
          <Route path="/" element={
            <ProtectedRoute roles={["admin","editor"]}>
              <Dashboard />
            </ProtectedRoute>
          } />

          <Route path="/admin" element={
            <ProtectedRoute roles={["admin"]}>
              <AdminArea />
            </ProtectedRoute>
          } />

          <Route path="/editor" element={
            <ProtectedRoute roles={["editor","admin"]}>
              <EditorArea />
            </ProtectedRoute>
          } />

          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>

      <footer className="footer">Built to implement OpenAPI endpoints. Only admin/editor allowed.</footer>
    </div>
  )
}