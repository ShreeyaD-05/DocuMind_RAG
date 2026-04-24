import React, { useRef } from 'react'

export default function Sidebar({ docs, onUpload, onClear, uploading, uploadProgress }) {
  const inputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) onUpload(file)
    e.target.value = ''
  }

  return (
    <aside
      className="w-72 flex-shrink-0 flex flex-col gap-4 p-4 overflow-y-auto"
      style={{
        background: 'linear-gradient(180deg, #0f1f4a 0%, #0B1220 100%)',
        borderRight: '1px solid rgba(96,165,250,0.12)',
      }}
    >
      {/* Upload button */}
      <div>
        <p className="text-xs font-semibold text-textSecondary uppercase tracking-widest mb-3">
          Documents
        </p>
        <button
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
          className="w-full py-3 rounded-2xl font-semibold text-white text-sm transition-all duration-300 relative overflow-hidden"
          style={{
            background: uploading
              ? 'linear-gradient(135deg, #1e3a8a88, #3b82f688)'
              : 'linear-gradient(135deg, #1E3A8A, #3B82F6)',
            boxShadow: uploading ? 'none' : '0 0 20px rgba(96,165,250,0.35)',
          }}
          onMouseEnter={(e) => {
            if (!uploading) e.currentTarget.style.boxShadow = '0 0 30px rgba(96,165,250,0.6)'
          }}
          onMouseLeave={(e) => {
            if (!uploading) e.currentTarget.style.boxShadow = '0 0 20px rgba(96,165,250,0.35)'
          }}
        >
          {uploading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="white" strokeWidth="4" />
                <path className="opacity-75" fill="white" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              Uploading {uploadProgress}%
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload Document
            </span>
          )}
        </button>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt,.md"
          className="hidden"
          onChange={handleFileChange}
        />
        <p className="text-xs text-textSecondary mt-1.5 text-center">PDF, TXT, MD supported</p>
      </div>

      {/* Progress bar */}
      {uploading && (
        <div className="w-full bg-gray-800 rounded-full h-1.5">
          <div
            className="h-1.5 rounded-full transition-all duration-300"
            style={{
              width: `${uploadProgress}%`,
              background: 'linear-gradient(90deg, #1E3A8A, #60A5FA)',
            }}
          />
        </div>
      )}

      {/* File list */}
      <div className="flex-1">
        <p className="text-xs font-semibold text-textSecondary uppercase tracking-widest mb-2">
          Indexed Files ({docs.length})
        </p>
        {docs.length === 0 ? (
          <div className="text-center py-8 text-textSecondary text-sm">
            <div className="text-3xl mb-2">📂</div>
            <p>No documents yet</p>
            <p className="text-xs mt-1">Upload a file to get started</p>
          </div>
        ) : (
          <ul className="flex flex-col gap-2">
            {docs.map((doc) => (
              <li
                key={doc.filename}
                className="glass rounded-xl px-3 py-2.5 flex items-start gap-2 transition-all duration-300 hover:border-accentGlow/30"
              >
                <span className="text-lg mt-0.5">
                  {doc.filename.endsWith('.pdf') ? '📄' : '📝'}
                </span>
                <div className="min-w-0">
                  <p className="text-sm text-textPrimary truncate font-medium">{doc.filename}</p>
                  <p className="text-xs text-textSecondary">
                    {doc.chunks} chunks · {(doc.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Clear all */}
      {docs.length > 0 && (
        <button
          onClick={onClear}
          className="w-full py-2.5 rounded-2xl text-sm font-medium text-red-400 border border-red-900/40 transition-all duration-300 hover:bg-red-900/20 hover:border-red-500/60 hover:text-red-300"
        >
          🗑 Clear All Documents
        </button>
      )}
    </aside>
  )
}
