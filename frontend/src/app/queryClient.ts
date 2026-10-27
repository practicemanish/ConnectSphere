import { QueryClient } from '@tanstack/react-query'

// One shared cache for all server data in the app.
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000, // treat data as fresh for 30s before refetching
      retry: 1,
    },
  },
})
