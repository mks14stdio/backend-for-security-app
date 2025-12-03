import React, { useEffect, useState } from 'react'
import api from '../../api'

export default function ArticlesManager(){
  const [articles, setArticles] = useState([])
  const [limit, setLimit] = useState(10)
  const [offset, setOffset] = useState(0)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState({content: '', test_pk: null})

  async function load(){
    try{
      // OpenAPI requires form-urlencoded body with limit/offset for GET /v1/article/
      const r = await api.get('/v1/article/', { data: { limit, offset } })
      setArticles(r.data || [])
    }catch(e){ console.error(e); alert('Failed to load articles') }
  }

  useEffect(()=>{ load() }, [])

  async function create(){
    try{
      const r = await api.post('/v1/article/', form)
      setArticles([r.data, ...articles])
      setForm({content:'', test_pk:null})
    }catch(e){ alert('Create failed: '+JSON.stringify(e.response?.data||e.message)) }
  }

  async function update(){
    try{
      const r = await api.patch(`/v1/article/${editing}/`, form)
      setArticles(articles.map(a=> a.id===r.data.id? r.data : a))
      setEditing(null)
      setForm({content:'', test_pk:null})
    }catch(e){ alert('Update failed') }
  }

  async function remove(id){
    if(!window.confirm('Delete?')) return
    try{ await api.delete(`/v1/article/${id}/`); setArticles(articles.filter(a=>a.id!==id)) }catch(e){ alert('Delete failed') }
  }

  return (
    <div className="card">
      <h3>Articles</h3>
      <div className="form-inline">
        <textarea placeholder="Content" value={form.content} onChange={e=>setForm({...form, content:e.target.value})} />
        <input placeholder="test_pk (optional)" value={form.test_pk||''} onChange={e=>setForm({...form, test_pk: e.target.value? Number(e.target.value): null})} />
        {editing ? <button className="btn" onClick={update}>Save</button> : <button className="btn" onClick={create}>Create</button>}
      </div>

      <ul className="list">
        {articles.map(a => (
          <li key={a.id} className="list-item">
            <div className="list-content">{a.content.slice(0,200)}{a.content.length>200?'...':''}</div>
            <div className="list-actions">
              <button className="btn small" onClick={()=>{ setEditing(a.id); setForm({content:a.content, test_pk: a.test_pk}) }}>Edit</button>
              <button className="btn small outline" onClick={()=>remove(a.id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}