import { createRootRouteWithContext } from "@tanstack/react-router";
import Layout from "../components/layout";
import type { UserContextType } from "../providers/user.provider";

type RouterContextType = {
  user: UserContextType,
}

export const rootRoute = createRootRouteWithContext<RouterContextType>()({
  component: Layout,
});
