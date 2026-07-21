import { useEffect, useState } from 'react'
import api from '../services/api'

export default function DashboardPage() {
  const [databases, setDatabases] = useState([])
  const [history, setHistory] = useState([])

  useEffect(() => {
    api.get('/schema').then(({ data }) => setDatabases(data))
    api.get('/history').then(({ data }) => setHistory(data))
  }, [])

  return (
    <div className="mx-auto max-w-7xl px-6 py-12">
      <h2 className="text-3xl font-semibold">Dashboard</h2>
      <div className="mt-8 grid gap-6 md:grid-cols-3">
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><p className="text-sm text-slate-400">Uploaded databases</p><p className="mt-2 text-3xl font-bold">{databases.length}</p></div>
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><p className="text-sm text-slate-400">Recent queries</p><p className="mt-2 text-3xl font-bold">{history.length}</p></div>
        <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><p className="text-sm text-slate-400">Tables total</p><p className="mt-2 text-3xl font-bold">{databases.reduce((n, d) => n + (d.metadata_json?.tables?.length || 0), 0)}</p></div>
      </div>

      <div className="mt-10 grid gap-6 xl:grid-cols-2">
        <section className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h3 className="text-lg font-semibold">Uploaded workspaces</h3>
          <div className="mt-4 space-y-4">
            {databases.map((db) => (
              <div key={db.id} className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium">{db.name}</p>
                    <p className="text-sm text-slate-400">{db.filename}</p>
                  </div>
                  <span className="rounded-full bg-teal-500/10 px-3 py-1 text-xs text-teal-300">{db.metadata_json?.tables?.length || 0} tables</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-3xl border border-white/10 bg-white/5 p-6">
          <h3 className="text-lg font-semibold">Recent history</h3>
          <div className="mt-4 space-y-4">
            {history.map((item) => (
              <div key={item.id} className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
                <p className="font-medium">{item.question}</p>
                <p className="mt-1 text-xs text-slate-400">{item.execution_time_ms || 0} ms · {item.success ? 'Success' : 'Failed'}</p>
                <pre className="mt-3 overflow-x-auto text-xs text-emerald-300">{item.generated_sql}</pre>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
