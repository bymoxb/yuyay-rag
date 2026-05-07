export type Response<T> = {
  ok: true,
  data: T,
} | {
  ok: false,
  error: string,
}


export type User = {
  email: string,
  fullName: string,
  roles: string[],
  functionalities: string[],
}

export type RoleMessageType = "user" | "assistant";

export type Message = {
  id: string,
  chatId: string,
  content: string,
  role: RoleMessageType,
}


export const Roles = {
  NORMAL: "role_user",
  ADMIN: "role_admin",
  REPORT: "role_report",
} as const
