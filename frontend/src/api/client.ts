// Thin wrapper around fetch. Every API call goes through here, so auth headers,
// error handling, and the base path are defined in one place.

export class ApiError extends Error {
  readonly status: number
  readonly body: unknown

  constructor(status: number, body: unknown) {
    super(`API request failed with status ${status}`)
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }
}

const API_BASE = '/api'

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { Accept: 'application/json' },
    credentials: 'same-origin', // send cookies (used from Phase 3)
  })

  const body: unknown = await response.json().catch(() => null)

  if (!response.ok) {
    throw new ApiError(response.status, body)
  }
  return body as T
}
