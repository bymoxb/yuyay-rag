import { RouterProvider } from '@tanstack/react-router'
import { router } from './router'
import { useOAuth } from './providers/oauth.provider';

function App() {
  const auth = useOAuth();
  return <RouterProvider router={router} context={{ auth }} />
}

export default App
