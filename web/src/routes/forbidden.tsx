import { createRoute } from "@tanstack/react-router";
import { rootRoute } from "./root";

export const forbiddenRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/forbidden",
  component: ForbiddenPage,
})

function ForbiddenPage() {
  return <div>Forbidden Page</div>
}
