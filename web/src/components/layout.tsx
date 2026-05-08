import { Link, Outlet } from "@tanstack/react-router";
import { useOAuth } from "../providers/oauth.provider";
import { Roles } from "../types";
import ChatHistory from "./ChatHistory";

export default function Layout() {
  const { hasRole, logout } = useOAuth()
  return (
    <>
      <aside className="py-2 gap-2">
        {
          hasRole(Roles.NORMAL) && <Link to="/">New Chat</Link>
        }
        {
          hasRole(Roles.NORMAL) && <ChatHistory />
        }
        {
          hasRole([Roles.REPORT, Roles.ADMIN]) && <Link to="/reports">Reports</Link>
        }
        <span className="flex-1"></span>
        <button className="hover:cursor-pointer" onClick={logout}>Cerrar Sesión</button>
      </aside>
      <main className="border mx-auto w-full h-full min-h-0">
        <Outlet />
      </main>
    </>
  )
}
