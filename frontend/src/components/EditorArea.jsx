import React from 'react'
import ArticlesManager from './content/ArticlesManager'
import ModulesManager from './content/ModulesManager'
import TestsManager from './content/TestsManager'

export default function EditorArea(){
  return (
    <div>
      <h2>Editor console</h2>
      <div className="grid">
        <ArticlesManager />
        <ModulesManager />
        <TestsManager />
      </div>
    </div>
  )
}