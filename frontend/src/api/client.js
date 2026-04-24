import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000, // LLM inference can be slow — 5 min for cold model load
})

export const uploadDocument = (file, onProgress) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress,
  })
}

export const queryDocuments = (question, top_k = 5) =>
  api.post('/query', { question, top_k })

export const listDocuments = () => api.get('/documents')

export const clearDocuments = () => api.delete('/clear')

export const healthCheck = () => api.get('/health')
