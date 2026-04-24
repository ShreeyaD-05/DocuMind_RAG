import React, { useState, useEffect, useCallback } from 'react'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import InputBox from './components/InputBox'
import { uploadDocument, queryDocuments, listDocuments, clearDocuments, healthCheck } from './api/client'

let msgIdCounter = 0
const newId = () => ++msgIdCounter

export default function App() {
  const [messages, setMessages] = useState([])
  const [docs, setDocs] = useState([])
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [toast, setToast] = useState(null)

  const showToast = (msg, type = 'info') => {
    setToast({ msg, type })
    setTimeout(() => setToast(null), 3500)
  }

  const refreshDocs = useCallback(async () => {
    try {
      const res = await listDocuments()
      setDocs(res.data)
    } catch {
      // silently fail
    }
  }, [])

  const refreshHealth = useCallback(async () => {
    try {
      const res = await healthCheck()
      setHealth(res.data)
    } catch {
      // silently fail
    }
  }, [])

  useEffect(() => {
    refreshDocs()
    refreshHealth()
    const interval = setInterval(refreshHealth, 30000)
    return () => clearInterval(interval)
  }, [refreshDocs, refreshHealth])

  const handleUpload = async (file) => {
    setUploading(true)
    setUploadProgress(0)
    try {
      await uploadDocument(file, (e) => {
        if (e.total) setUploadProgress(Math.round((e.loaded / e.total) * 100))
      })
      showToast(`"${file.name}" uploaded and indexed.`, 'success')
      await refreshDocs()
      await refreshHealth()
    } catch (err) {
      const detail = err.response?.data?.detail || 'Upload failed.'
      showToast(detail, 'error')
    } finally {
      setUploading(false)
      setUploadProgress(0)
    }
  }

  const handleClear = async () => {
    if (!window.confirm('Clear all documents and chat history?')) return
    try {
      await clearDocuments()
      setDocs([])
      setMessages([])
      setHealth(null)
      showToast('All documents cleared.', 'info')
      await refreshHealth()
    } catch {
      showToast('Failed to clear documents.', 'error')
    }
  }

  const handleSend = async (question) => {
    const userMsg = {
      id: newId(),
      role: 'user',
      content: question,
      timestamp: Date.now(),
    }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)

    try {
      const res = await queryDocuments(question)
      const { answer, sources } = res.data
      const aiMsg = {
        id: newId(),
        role: 'assistant',
        content: answer,
        sources,
        timestamp: Date.now(),
      }
      setMessages((prev) => [...prev, aiMsg])
    } catch (err) {
      const detail = err.response?.data?.detail || 'Something went wrong. Please try again.'
      const errMsg = {
        id: newId(),
        role: 'assistant',
        content: `⚠️ ${detail}`,
        sources: [],
        timestamp: Date.now(),
      }
      setMessages((prev) => [...prev, errMsg])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col overflow-hidden" style={{ background: '#0B1220' }}>
      <Navbar health={health} />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          docs={docs}
          onUpload={handleUpload}
          onClear={handleClear}
          uploading={uploading}
          uploadProgress={uploadProgress}
        />

        <main className="flex-1 flex flex-col overflow-hidden">
          <ChatArea messages={messages} loading={loading} />
          <InputBox onSend={handleSend} disabled={loading} />
        </main>
      </div>

      {/* Toast notification */}
      {toast && (
        <div
          className="fixed bottom-6 right-6 px-4 py-3 rounded-2xl text-sm font-medium shadow-xl fade-in-up z-50"
          style={{
            background:
              toast.type === 'success'
                ? 'linear-gradient(135deg, #065f46, #059669)'
                : toast.type === 'error'
                ? 'linear-gradient(135deg, #7f1d1d, #dc2626)'
                : 'linear-gradient(135deg, #1E3A8A, #3B82F6)',
            color: '#F9FAFB',
            boxShadow: '0 8px 30px rgba(0,0,0,0.4)',
          }}
        >
          {toast.type === 'success' ? '✅' : toast.type === 'error' ? '❌' : 'ℹ️'} {toast.msg}
        </div>
      )}
    </div>
  )
}
