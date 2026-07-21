import { useState } from 'react'
import api from '../services/api'

export default function UploadPage() {
  const [name, setName] = useState('')
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!name || !file) return
    const formData = new FormData()
    formData.append('name', name)
    formData.append('file', file)
    try {
      setLoading(true)
      const { data } = await api.post('/upload', formData)
      setMessage(`Imported ${data.tables.length} tables into ${data.schema_name}`)
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <h2 className="text-3xl font-semibold">Upload SQL</h2>
      <p className="mt-2 text-slate-400">Import a schema or dump file into PostgreSQL.</p>
      <form onSubmit={handleUpload} className="mt-8 space-y-6 rounded-3xl border border-white/10 bg-white/5 p-6">
        <input className="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3" placeholder="Workspace name" value={name} onChange={(e) => setName(e.target.value)} />
        <input type="file" accept=".sql" onChange={(e) => setFile(e.target.files?.[0] || null)} className="block w-full rounded-xl border border-dashed border-white/15 bg-slate-950 p-4" />
        <button className="rounded-xl bg-teal-600 px-5 py-3 text-sm font-medium text-white">{loading ? 'Uploading...' : 'Upload and import'}</button>
        {message && <div className="text-sm text-slate-300">{message}</div>}
      </form>
    </div>
  )
}
