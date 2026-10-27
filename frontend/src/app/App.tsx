import { QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider } from 'react-router/dom'
import { queryClient } from './queryClient.ts'
import { router } from './router.tsx'

// Root component: wires up app-wide providers. Pages live under the router.
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  )
}
