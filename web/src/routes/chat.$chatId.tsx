import { createRoute, redirect } from "@tanstack/react-router";
import { rootRoute } from "./root";
import { Roles } from "../types";

export const chatIdRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/chat/$chatId",
  component: ChatIdPage,
  beforeLoad: ({ context }) => {
    if (!context.auth.hasRole(Roles.NORMAL)) {
      throw redirect({ to: "/forbidden" });
    }
  }
})

function ChatIdPage() {
  const { chatId } = chatIdRoute.useParams()

  return (
    <pre>{JSON.stringify({ chatId })}</pre>
  )
}
