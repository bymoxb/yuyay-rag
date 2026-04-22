import { Link, Outlet } from "@tanstack/react-router";
import { useOAuth } from "../providers/oauth.provider";
import { Roles } from "../types";

export default function Layout() {
  const { hasRole, logout } = useOAuth()
  return (
    <main className="container border mx-auto flex flex-col h-full min-h-0">
      <header className="flex gap-2">
        {
          hasRole(Roles.NORMAL) && <Link to="/">Chat</Link>
        }
        {
          hasRole([Roles.REPORT, Roles.ADMIN]) && <Link to="/reports">Reports</Link>
        }
        <span className="flex-1"></span>
        <button onClick={logout}>Cerrar Sesión</button>
      </header>
      <Outlet />
    </main>
  )
}
