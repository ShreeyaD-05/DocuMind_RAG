import React, { useEffect, useRef } from 'react'
import ChatMessage from './ChatMessage'
import TypingIndicator from './TypingIndicator'

export default function ChatArea({ messages, loading }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-5">
      {messages.length === 0 && !loading && (
        <div className="flex-1 flex flex-col items-center justify-center text-center py-16">
          <div className="text-6xl mb-4">🧠</div>
          <h2 className="text-2xl font-bold text-textPrimary mb-2">Ask DocuMind</h2>
          <p className="text-textSecondary max-w-sm">
            Upload documents in the sidebar, then ask questions about their content.
          </p>
          <div className="mt-6 flex flex-wrap gap-2 justify-center">
            {[
              'What is the main topic?',
              'Summarize the key points',
              'What are the conclusions?',
            ].map((hint) => (
              <span
                key={hint}
                className="px-3 py-1.5 rounded-full text-xs text-accentGlow"
                style={{ background: 'rgba(96,165,250,0.08)', border: '1px solid rgba(96,165,250,0.2)' }}
              >
                {hint}
              </span>
            ))}
          </div>
        </div>
      )}

      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg} />
      ))}

      {loading && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  )
}
