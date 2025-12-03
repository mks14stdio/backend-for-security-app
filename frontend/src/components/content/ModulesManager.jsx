import React, { useState, useEffect } from 'react'
import api from '../../api'

export default function ModulesManager(){
  const [moduleId, setModuleId] = useState('')
  const [module, setModule] = useState(null)
  const [form, setForm] = useState({title:'', items:[]})
  const [itemForm, setItemForm] = useState({title:'', article_id:''})

  async function create(){
    try{ const r = await api.post('/v1/module/', form); alert('Module created: '+JSON.stringify(r.data)) }catch(e){ alert('Create module failed') }
  }

  async function getModule(){
    try{ const r = await api.get(`/v1/module/${moduleId}`); setModule(r.data) }catch(e){ alert('Get failed') }
  }

  async function addItem(){
    try{ await api.post(`/v1/module/${moduleId}/`, { title: itemForm.title, article_id: Number(itemForm.article_id) }); alert('Item added'); getModule() }catch(e){ alert('Add item failed') }
  }

  async function updateModule(){
    try{ const r = await api.patch(`/v1/module/${moduleId}/`, { title: form.title }); setModule(r.data); alert('Updated') }catch(e){ alert('Update failed') }
  }

  async function deleteModule(){ if(!window.confirm('Delete module?')) return; try{ await api.delete(`/v1/module/${moduleId}/`); setModule(null); alert('Deleted') }catch(e){ alert('Delete failed') } }

  async function deleteItem(item_id){ if(!window.confirm('Delete item?')) return; try{ await api.delete(`/v1/module/${moduleId}/item/${item_id}/`); alert('Deleted'); getModule() }catch(e){ alert('Delete item failed') } }

  return (
    <div className="card">
      <h3>Modules</h3>
      <div className="form">
        <label>New module title<input value={form.title} onChange={e=>setForm({...form, title:e.target.value})} /></label>
        <label>Items (json array of {{ title: itemForm.title, article_id: Number(itemForm.article_id) }})<textarea value={JSON.stringify(form.items)} onChange={e=>{try{setForm({...form, items: JSON.parse(e.target.value)})}catch(_){} }} /></label>
        <button className="btn" onClick={create}>Create Module</button>
      </div>

      <hr />
      <div>
        <input placeholder="module id" value={moduleId} onChange={e=>setModuleId(e.target.value)} />
        <button className="btn small" onClick={getModule}>Get</button>
        <button className="btn small outline" onClick={deleteModule}>Delete module</button>
      </div>

      {module && (
        <div className="module-view">
          <h4>{module.title} (#{module.id})</h4>
          <div className="module-items">
            {module.items?.map(it=> (
              <div key={it.order_index} className="module-item">
                <div>{it.title} — article #{it.article_id}</div>
                <button className="btn small outline" onClick={()=>deleteItem(it.order_index)}>Delete item</button>
              </div>
            ))}
            <div className="form-inline">
              <input placeholder="item title" value={itemForm.title} onChange={e=>setItemForm({...itemForm, title:e.target.value})} />
              <input placeholder="article id" value={itemForm.article_id} onChange={e=>setItemForm({...itemForm, article_id:e.target.value})} />
              <button className="btn" onClick={addItem}>Add item</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}