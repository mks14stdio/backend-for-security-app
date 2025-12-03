import React, { useState } from 'react'
import api from '../../api'

export default function TestsManager(){
  const [title, setTitle] = useState('')
  const [questionsCount, setQuestionsCount] = useState(0)
  const [questions, setQuestions] = useState([])
  const [testId, setTestId] = useState('')

  function addQuestion(){ setQuestions([...questions, { text:'', type:'single', answers: [{text:'', is_correct:false}]}]) }

  async function create(){
    try{
      const r = await api.post('/v1/test/', { title, questions_count: questionsCount, questions })
      alert('Created test id: '+(r.data?.id||'unknown'))
    }catch(e){ alert('Create failed') }
  }

  async function getTest(){ try{ const r = await api.get(`/v1/test/${testId}/`); alert('Test: '+JSON.stringify(r.data)) }catch(e){ alert('Get failed') } }
  async function deleteTest(){ if(!window.confirm('Delete test?')) return; try{ await api.delete(`/v1/test/${testId}/`); alert('Deleted') }catch(e){ alert('Delete failed') } }

  return (
    <div className="card">
      <h3>Tests</h3>
      <div className="form">
        <label>Title<input value={title} onChange={e=>setTitle(e.target.value)} /></label>
        <label>Questions count<input type="number" value={questionsCount} onChange={e=>setQuestionsCount(Number(e.target.value))} /></label>
        <div>
          <button className="btn" onClick={addQuestion}>Add question</button>
        </div>
        {questions.map((q,idx)=> (
          <div key={idx} className="question-block">
            <input placeholder="Text" value={q.text} onChange={e=>{ const copy=[...questions]; copy[idx].text=e.target.value; setQuestions(copy) }} />
            <select value={q.type} onChange={e=>{ const copy=[...questions]; copy[idx].type=e.target.value; setQuestions(copy) }}>
              <option value="single">single</option>
              <option value="multiple">multiple</option>
              <option value="text">text</option>
            </select>
            <div>
              {q.answers.map((a,i)=> (
                <div key={i} className="answer-row">
                  <input placeholder="answer" value={a.text} onChange={e=>{ const copy=[...questions]; copy[idx].answers[i].text=e.target.value; setQuestions(copy) }} />
                  <label><input type="checkbox" checked={a.is_correct} onChange={e=>{ const copy=[...questions]; copy[idx].answers[i].is_correct=e.target.checked; setQuestions(copy) }} /> correct</label>
                </div>
              ))}
              <button className="btn small" onClick={()=>{ const copy=[...questions]; copy[idx].answers.push({text:'', is_correct:false}); setQuestions(copy) }}>Add answer</button>
            </div>
          </div>
        ))}
        <button className="btn" onClick={create}>Create test</button>
      </div>

      <hr />
      <div>
        <input placeholder="test id" value={testId} onChange={e=>setTestId(e.target.value)} />
        <button className="btn small" onClick={getTest}>Get</button>
        <button className="btn small outline" onClick={deleteTest}>Delete</button>
      </div>
    </div>
  )
}
