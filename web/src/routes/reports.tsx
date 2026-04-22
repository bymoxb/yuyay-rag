import { createRoute, redirect } from "@tanstack/react-router";
import { rootRoute } from "./root";
import { Roles } from "../types";

export const reportRoute = createRoute({
  getParentRoute: () => rootRoute,
  component: ReportPage,
  path: "/reports",
  beforeLoad: ({ context }) => {
    if (!context.auth.hasRole([Roles.REPORT, Roles.ADMIN])) {
      throw redirect({ to: "/" });
    }
  }
})

export default function ReportPage() {
  return <div>Report Page</div>
}

