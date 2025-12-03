import React, { useEffect, useState } from 'react'
import api from '../api'

export default function AdminArea() {
  const [users, setUsers] = useState([])
  const [form, setForm] = useState({ role: 'user', first_name: '', last_name: '', email: '', password: '' })
  const [qEmail, setQEmail] = useState('')
  useEffect(()=>{ fetchUsers() }, [])

  async function fetchUsers() {
    try {
      // no endpoint for listing users in OpenAPI, but we have create and get_by_email
      // We'll attempt to search by email when needed; for admin UX keep a small manual list from created users
    } catch(e){}
  }

  async function createUser(e){
    e.preventDefault()
    try{
      await api.post(`/v1/users/?role=${form.role}`, {
        first_name: form.first_name,
        last_name: form.last_name,
        email: form.email,
        password: form.password
      })
      alert('User created')
    }catch(e){ alert('Create user failed: '+JSON.stringify(e.response?.data || e.message)) }
  }

  async function search() {
    try{
      const r = await api.get('/v1/users/', { params: { email: qEmail } })
      alert('User: '+JSON.stringify(r.data))
    }catch(e){ alert('Not found') }
  }

  return (
    <div className="card">
      <h2>Admin — Users</h2>
      <form className="form" onSubmit={createUser}>
        <label>Role
          <select value={form.role} onChange={e=>setForm({...form, role: e.target.value})}>
            <option value="user">user</option>
            <option value="editor">editor</option>
            <option value="admin">admin</option>
          </select>
        </label>
        <label>First name<input value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})} required /></label>
        <label>Last name<input value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})} required /></label>
        <label>Email<input value={form.email} onChange={e=>setForm({...form, email:e.target.value})} type="email" required /></label>
        <label>Password<input value={form.password} onChange={e=>setForm({...form, password:e.target.value})} minLength={8} required type="password"/></label>
        <button className="btn">Create user</button>
      </form>

      <hr />

      <div>
        <h3>Search by email</h3>
        <input value={qEmail} onChange={e=>setQEmail(e.target.value)} placeholder="email@example.com" />
        <button className="btn small" onClick={search}>Search</button>
      </div>
    </div>
  )
}