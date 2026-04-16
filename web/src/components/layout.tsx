import { Link, Outlet } from "@tanstack/react-router";
import { useUserContext } from "../providers/user.provider";
import { useOAuth } from "../providers/oauth.provider";

export default function Layout() {
  const { functionalities } = useUserContext()
  const { logout } = useOAuth()
  return (
    <main className="container border mx-auto flex flex-col h-full min-h-0">
      <header className="flex gap-2">
        {
          functionalities.includes('chat') && <Link to="/">Chat</Link>
        }
        {
          functionalities.includes('report') && <Link to="/reports">Reports</Link>
        }
        {
          functionalities.some(item => item.startsWith('user.')) && <Link to="/users">Users</Link>
        }
        <span className="flex-1"></span>
        <button onClick={logout}>Cerrar Sesión</button>
      </header>
      <Outlet />
    </main>
  )
}
