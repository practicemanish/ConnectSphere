import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import HealthStatus from './HealthStatus.tsx'

function renderWithQueryClient(ui: React.ReactElement) {
  // Fresh cache per test so results don't leak between tests.
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>)
}

function mockFetchResponse(status: number, body: unknown) {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue(new Response(JSON.stringify(body), { status })),
  )
}

describe('HealthStatus', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('shows healthy status when the API reports ok', async () => {
    mockFetchResponse(200, { status: 'ok', database: 'ok' })

    renderWithQueryClient(<HealthStatus />)

    expect(await screen.findByText('API ok · database ok')).toBeInTheDocument()
    expect(fetch).toHaveBeenCalledWith('/api/health', expect.any(Object))
  })

  it('shows an error when the API returns 503', async () => {
    mockFetchResponse(503, { status: 'degraded', database: 'unavailable' })

    renderWithQueryClient(<HealthStatus />)

    expect(await screen.findByText('Backend or database unavailable')).toBeInTheDocument()
  })
})
