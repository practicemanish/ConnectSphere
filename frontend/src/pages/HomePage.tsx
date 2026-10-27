import HealthStatus from '../features/health/HealthStatus.tsx'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50 px-4 py-12">
      <div className="mx-auto max-w-xl space-y-6">
        <header>
          <h1 className="text-3xl font-bold text-gray-900">ConnectSphere</h1>
          <p className="mt-1 text-gray-600">Project skeleton — Phase 1</p>
        </header>
        <HealthStatus />
      </div>
    </main>
  )
}
