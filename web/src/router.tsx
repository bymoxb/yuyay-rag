import { createRouter } from "@tanstack/react-router";
import { chatRoute } from "./routes/chat";
import { forbiddenRoute } from "./routes/forbidden";
import { reportRoute } from "./routes/reports";
import { rootRoute } from "./routes/root";
import { usersRoute } from "./routes/users";

const routeTree = rootRoute.addChildren([
  chatRoute,
  reportRoute,
  usersRoute,
  forbiddenRoute,
])

export const router = createRouter({ routeTree, context: { user: null! } })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
