import React from 'react'

export default function TypingIndicator() {
  return (
    <div className="flex items-start gap-3 fade-in-up">
      <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm"
        style={{ background: 'linear-gradient(135deg, #1E3A8A, #3B82F6)' }}>
        🧠
      </div>
      <div
        className="px-4 py-3 rounded-2xl rounded-tl-sm"
        style={{ background: '#1F2937', border: '1px solid rgba(96,165,250,0.15)' }}
      >
        <span className="dot-bounce text-accentGlow text-xl">•</span>
        <span className="dot-bounce text-accentGlow text-xl">•</span>
        <span className="dot-bounce text-accentGlow text-xl">•</span>
      </div>
    </div>
  )
}
