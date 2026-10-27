import { Link } from 'react-router'

export default function NotFoundPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-gray-50 px-4">
      <h1 className="text-2xl font-semibold text-gray-900">Page not found</h1>
      <Link to="/" className="text-blue-600 hover:underline">
        Go home
      </Link>
    </main>
  )
}
