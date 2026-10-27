import { useQuery } from '@tanstack/react-query'
import { apiGet } from '../../api/client.ts'

// Mirrors backend/app/modules/health/schemas.py -> HealthResponse
export type HealthResponse = {
  status: 'ok' | 'degraded'
  database: 'ok' | 'unavailable'
}

export function useHealth() {
  return useQuery({
    queryKey: ['health'], // cache key: same key = same cached data
    queryFn: () => apiGet<HealthResponse>('/health'),
    retry: false, // show a failure immediately instead of retrying
  })
}
