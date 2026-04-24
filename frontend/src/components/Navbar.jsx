import React from 'react'

export default function Navbar({ health }) {
  return (
    <nav
      className="flex items-center justify-between px-6 py-3 z-10 flex-shrink-0"
      style={{
        background: 'linear-gradient(90deg, #1E3A8A 0%, #1d4ed8 50%, #2563eb 100%)',
        boxShadow: '0 2px 20px rgba(30,58,138,0.6)',
      }}
    >
      <div className="flex items-center gap-3">
        <span className="text-2xl">🧠</span>
        <div>
          <h1 className="text-xl font-bold text-white tracking-wide">DocuMind</h1>
          <p className="text-xs text-blue-200">AI Document Intelligence</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {health && (
          <div className="flex items-center gap-2 text-sm text-blue-100">
            <span className="w-2 h-2 rounded-full bg-green-400 inline-block" />
            <span>{health.documents_loaded} doc{health.documents_loaded !== 1 ? 's' : ''}</span>
            <span className="text-blue-300">·</span>
            <span>{health.index_size} chunks</span>
          </div>
        )}
        <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-xs text-blue-100">
          <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
          RAG Online
        </div>
      </div>
    </nav>
  )
}
