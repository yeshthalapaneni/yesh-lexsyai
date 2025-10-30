import axios from 'axios'


export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'


export async function uploadDoc(file) {
const fd = new FormData()
fd.append('file', file)
const { data } = await axios.post(`${API_BASE}/extract`, fd, {
headers: { 'Content-Type': 'multipart/form-data' }
})
return data
}


export async function getSession(sessionId) {
const { data } = await axios.get(`${API_BASE}/session/${sessionId}`)
return data
}


export async function sendAnswer(sessionId, placeholderId, message) {
const { data } = await axios.post(`${API_BASE}/chat`, { session_id: sessionId, placeholder_id: placeholderId, message })
return data
}


export function downloadUrl(sessionId) {
return `${API_BASE}/download/${sessionId}`
}
