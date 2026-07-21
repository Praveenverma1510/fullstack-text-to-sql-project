import { useEffect, useState } from 'react'
import api from '../services/api'

export default function QueryPage() {
  const [databases, setDatabases] = useState([])
  const [databaseId, setDatabaseId] = useState('')
  const [question, setQuestion] = useState('')
  const [generatedSql, setGeneratedSql] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.get('/schema').then(({ data }) => {
      setDatabases(data)
      if (data.length) setDatabaseId(String(data[0].id))
    })
  }, [])

  const handleGenerate = async () => {
    try {
      setLoading(true)
      setError('')
      const { data } = await api.post('/generate-sql', { database_id: Number(databaseId), question })
      setGeneratedSql(data.generated_sql)
    } catch (err) {
      setError(err.response?.data?.detail || 'Generation failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRun = async () => {
    try {
      setLoading(true)
      setError('')
      const { data } = await api.post('/execute-query', {
        database_id: Number(databaseId),
        question,
        sql: generatedSql,
        limit: 100,
      })
      setResult(data)
      if (!data.success) setError(data.error_message || 'Execution failed')
    } catch (err) {
      setError(err.response?.data?.detail || 'Execution failed')
    } finally {
      setLoading(false)
    }
  }

  const downloadCsv = () => {
    if (!result?.rows?.length) return
    const headers = Object.keys(result.rows[0])
    const csv = [headers.join(','), ...result.rows.map(row => headers.map(h => JSON.stringify(row[h] ?? '')).join(','))].join('\n')
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'query-results.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-12">
      <h2 className="text-3xl font-semibold">Query workspace</h2>
      <div className="mt-8 grid gap-6 xl:grid-cols-2">
        <section className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <select value={databaseId} onChange={(e) => setDatabaseId(e.target.value)} className="w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3">
            <option value="">Select workspace</option>
            {databases.map((db) => <option key={db.id} value={db.id}>{db.name}</option>)}
          </select>
          <textarea rows={5} value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Show all customers from Mumbai" className="mt-4 w-full rounded-xl border border-white/10 bg-slate-950 px-4 py-3" />
          <div className="mt-4 flex flex-wrap gap-3">
            <button onClick={handleGenerate} className="rounded-xl bg-teal-600 px-5 py-3 text-sm text-white">{loading ? 'Working...' : 'Generate SQL'}</button>
            <button onClick={handleRun} className="rounded-xl border border-white/10 px-5 py-3 text-sm">Run Query</button>
            <button onClick={() => { setQuestion(''); setGeneratedSql(''); setResult(null); setError('') }} className="rounded-xl border border-white/10 px-5 py-3 text-sm">Clear</button>
            <button onClick={downloadCsv} className="rounded-xl border border-white/10 px-5 py-3 text-sm">Download CSV</button>
          </div>
          {error && <div className="mt-4 text-sm text-rose-300">{error}</div>}
        </section>

        <section className="space-y-6">
          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <div className="flex items-center justify-between gap-4">
              <h3 className="text-lg font-semibold">Generated SQL</h3>
              <button onClick={() => navigator.clipboard.writeText(generatedSql)} className="rounded-lg border border-white/10 px-3 py-2 text-xs">Copy</button>
            </div>
            <pre className="mt-3 overflow-x-auto rounded-2xl bg-slate-950 p-4 text-sm text-emerald-300">{generatedSql || '-- SQL will appear here --'}</pre>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <div className="flex items-center justify-between gap-4">
              <h3 className="text-lg font-semibold">Results</h3>
              <span className="text-xs text-slate-400">{result?.execution_time_ms ?? 0} ms</span>
            </div>
            {result?.rows?.length ? (
              <div className="mt-4 overflow-auto rounded-2xl border border-white/10">
                <table className="min-w-full text-sm">
                  <thead className="bg-slate-900 text-left text-slate-300">
                    <tr>{result.columns.map((col) => <th key={col} className="px-4 py-3">{col}</th>)}</tr>
                  </thead>
                  <tbody>
                    {result.rows.map((row, idx) => (
                      <tr key={idx} className="border-t border-white/10 bg-slate-950/60">
                        {result.columns.map((col) => <td key={col} className="px-4 py-3">{String(row[col] ?? '')}</td>)}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <pre className="mt-3 overflow-x-auto rounded-2xl bg-slate-950 p-4 text-xs text-slate-300">{JSON.stringify(result, null, 2) || 'No results yet'}</pre>
            )}
          </div>
        </section>
      </div>
    </div>
  )
}
