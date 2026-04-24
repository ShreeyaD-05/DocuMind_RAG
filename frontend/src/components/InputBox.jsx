import React, { useState, useRef, useEffect } from 'react'

export default function InputBox({ onSend, disabled }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  const handleSend = () => {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = Math.min(el.scrollHeight, 120) + 'px'
    }
  }, [value])

  return (
    <div
      className="px-6 py-4 flex-shrink-0"
      style={{
        background: 'rgba(11,18,32,0.95)',
        borderTop: '1px solid rgba(96,165,250,0.1)',
        animation: 'fadeInUp 0.4s ease',
      }}
    >
      <div
        className="flex items-end gap-3 rounded-2xl px-4 py-3 transition-all duration-300"
        style={{
          background: '#111827',
          border: '1px solid rgba(96,165,250,0.2)',
        }}
        onFocus={() => {}}
      >
        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={disabled ? 'Waiting for response...' : 'Ask a question about your documents...'}
          className="flex-1 bg-transparent text-textPrimary placeholder-textSecondary text-sm resize-none outline-none leading-relaxed"
          style={{ maxHeight: '120px' }}
        />
        <button
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-300"
          style={{
            background:
              disabled || !value.trim()
                ? 'rgba(30,58,138,0.3)'
                : 'linear-gradient(135deg, #1E3A8A, #3B82F6)',
            boxShadow:
              disabled || !value.trim() ? 'none' : '0 0 12px rgba(96,165,250,0.4)',
            cursor: disabled || !value.trim() ? 'not-allowed' : 'pointer',
          }}
          onMouseEnter={(e) => {
            if (!disabled && value.trim())
              e.currentTarget.style.boxShadow = '0 0 20px rgba(96,165,250,0.7)'
          }}
          onMouseLeave={(e) => {
            if (!disabled && value.trim())
              e.currentTarget.style.boxShadow = '0 0 12px rgba(96,165,250,0.4)'
          }}
        >
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
      <p className="text-xs text-textSecondary mt-2 text-center">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  )
}
