import UploadPage from "./UploadPage";

export default function HomePage() {
  return (<>
    <div className="mx-auto max-w-6xl px-2 py-4">
      <div className="rounded-3xl from-slate-900 to-slate-800 p-4">
        <p className="text-sm uppercase tracking-[0.2em] text-teal-400">AI powered data explorer</p>
        <h1 className="mt-4 text-4xl font-bold">Upload SQL dumps and query them in plain English.</h1>
        <p className="mt-4 max-w-3xl text-slate-300">
          Import PostgreSQL-compatible schema files, extract metadata, generate SQL with an open-source Hugging Face model,
          validate queries for safety, and execute read-only analytics against your uploaded workspace.
        </p>
        <UploadPage />
      </div>
    </div>

  </>
  )
}
