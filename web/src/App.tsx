import { RouterProvider } from '@tanstack/react-router'
import { router } from './router'
import { useUserContext } from './providers/user.provider'

function App() {
  const user = useUserContext();
  return <RouterProvider router={router} context={{ user }} />
}

export default App
