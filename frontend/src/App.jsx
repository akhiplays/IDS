import React from 'react'
import Dashboard from './components/Dashboard'

export default function App(){
  return (
    <div className="min-h-screen bg-[#0b1020] text-cyan-200">
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold text-cyan-300 mb-4">AI-IDS Dashboard</h1>
        <Dashboard />
      </div>
    </div>
  )
}
