import { createRoute, redirect } from "@tanstack/react-router"
import { rootRoute } from "./root"

export const usersRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/users",
  component: UsersPage,
  beforeLoad: ({ context }) => {
    if (!context.user.functionalities.some(item => item.startsWith('user.'))) {
      throw redirect({ to: "/" });
    }
  }
})

function UsersPage() {
  return <div>Users Page</div>
}
