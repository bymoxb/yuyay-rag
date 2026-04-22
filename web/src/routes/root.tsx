import { createRootRouteWithContext } from "@tanstack/react-router";
import Layout from "../components/layout";
import type { OAuthContextType } from "../providers/oauth.provider";

type RouterContextType = {
  auth: OAuthContextType,
}

export const rootRoute = createRootRouteWithContext<RouterContextType>()({
  component: Layout,
});
