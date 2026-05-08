import { createRouter } from "@tanstack/react-router";
import { chatRoute } from "./routes/chat";
import { forbiddenRoute } from "./routes/forbidden";
import { reportRoute } from "./routes/reports";
import { rootRoute } from "./routes/root";
import { chatIdRoute } from "./routes/chat.$chatId";

const routeTree = rootRoute.addChildren([
  chatRoute,
  chatIdRoute,
  reportRoute,
  forbiddenRoute,
])

export const router = createRouter({ routeTree, context: { auth: null! } })

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
