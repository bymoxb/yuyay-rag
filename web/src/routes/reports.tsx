import { createRoute, redirect } from "@tanstack/react-router";
import { rootRoute } from "./root";

export const reportRoute = createRoute({
  getParentRoute: () => rootRoute,
  component: ReportPage,
  path: "/reports",
  beforeLoad: ({ context }) => {
    if (!context.user.functionalities.includes('report')) {
      throw redirect({ to: "/" });
    }
  }
})

export default function ReportPage() {
  return <div>Report Page</div>
}

