import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  const [showSources, setShowSources] = useState(false)

  return (
    <div className={`flex items-start gap-3 fade-in-up ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold"
        style={{
          background: isUser
            ? 'linear-gradient(135deg, #1E3A8A, #2563eb)'
            : 'linear-gradient(135deg, #1E3A8A, #3B82F6)',
        }}
      >
        {isUser ? '👤' : '🧠'}
      </div>

      <div className={`flex flex-col gap-1 max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Bubble */}
        <div
          className="px-4 py-3 rounded-2xl text-sm leading-relaxed"
          style={
            isUser
              ? {
                  background: 'linear-gradient(135deg, #1E3A8A, #2563eb)',
                  borderRadius: '1rem 1rem 0.25rem 1rem',
                  color: '#F9FAFB',
                  boxShadow: '0 4px 15px rgba(30,58,138,0.4)',
                }
              : {
                  background: '#1F2937',
                  borderRadius: '1rem 1rem 1rem 0.25rem',
                  color: '#F9FAFB',
                  border: '1px solid rgba(96,165,250,0.15)',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
                }
          }
        >
          {isUser ? (
            message.content
          ) : (
            <ReactMarkdown
              components={{
                h1: ({node, ...props}) => <h1 className="text-base font-bold mt-2 mb-1" {...props} />,
                h2: ({node, ...props}) => <h2 className="text-sm font-bold mt-2 mb-1 text-blue-300" {...props} />,
                h3: ({node, ...props}) => <h3 className="text-sm font-semibold mt-1 mb-1" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc list-outside ml-4 space-y-1 my-1" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal list-outside ml-4 space-y-1 my-1" {...props} />,
                li: ({node, ...props}) => <li className="leading-relaxed" {...props} />,
                p: ({node, ...props}) => <p className="mb-1 leading-relaxed" {...props} />,
                strong: ({node, ...props}) => <strong className="font-semibold text-blue-200" {...props} />,
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {/* Sources toggle */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="w-full">
            <button
              onClick={() => setShowSources((s) => !s)}
              className="text-xs text-accentGlow hover:text-secondary transition-colors duration-200 flex items-center gap-1 mt-1"
            >
              <svg className={`w-3 h-3 transition-transform duration-200 ${showSources ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              {showSources ? 'Hide' : 'Show'} {message.sources.length} source{message.sources.length !== 1 ? 's' : ''}
            </button>
            {showSources && (
              <div className="mt-2 flex flex-col gap-1.5">
                {message.sources.map((src, i) => (
                  <div
                    key={i}
                    className="text-xs text-textSecondary px-3 py-2 rounded-xl"
                    style={{ background: 'rgba(96,165,250,0.06)', border: '1px solid rgba(96,165,250,0.12)' }}
                  >
                    <span className="text-accentGlow font-medium">#{i + 1}</span> {src}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <span className="text-xs text-textSecondary px-1">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  )
}
