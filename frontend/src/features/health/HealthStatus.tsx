import { useHealth } from './useHealth.ts'

export default function HealthStatus() {
  const { data, isPending, isError, refetch, isFetching } = useHealth()

  let label: string
  let dotClass: string
  if (isPending) {
    label = 'Checking backend…'
    dotClass = 'bg-gray-400'
  } else if (isError) {
    // Covers both "API down" and a 503 from the API (database unreachable).
    label = 'Backend or database unavailable'
    dotClass = 'bg-red-500'
  } else {
    label = `API ${data.status} · database ${data.database}`
    dotClass = 'bg-green-500'
  }

  return (
    <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-sm">
      <span className={`h-3 w-3 shrink-0 rounded-full ${dotClass}`} aria-hidden="true" />
      <p role="status" className="text-sm text-gray-800">
        {label}
      </p>
      <button
        type="button"
        onClick={() => refetch()}
        disabled={isFetching}
        className="ml-auto rounded-md px-3 py-1 text-sm font-medium text-blue-600 hover:bg-blue-50 disabled:opacity-50"
      >
        Recheck
      </button>
    </div>
  )
}
