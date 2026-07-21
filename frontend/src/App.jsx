import { NavLink, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import DashboardPage from './pages/DashboardPage'
import QueryPage from './pages/QueryPage'

export default function App() {
  const navClass = ({ isActive }) =>
    `block rounded-xl px-4 py-3 text-sm ${isActive ? 'bg-teal-600 text-white' : 'text-slate-300 hover:bg-white/5'}`

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex min-h-screen">
        <aside className="hidden w-72 border-r border-white/10 bg-slate-900/80 p-6 lg:block">
          <h1 className="text-xl font-semibold">Text To SQL</h1>
          <p className="mt-1 text-sm text-slate-400">Natural language to SQL data explorer</p>
          <nav className="mt-8 space-y-2">
            <NavLink to="/" className={navClass}>Home</NavLink>
            {/* <NavLink to="/upload" className={navClass}>Upload</NavLink> */}
            <NavLink to="/dashboard" className={navClass}>Dashboard</NavLink>
            <NavLink to="/query" className={navClass}>Query</NavLink>
          </nav>
        </aside>
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/query" element={<QueryPage />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}
