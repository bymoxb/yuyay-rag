export type Response<T> = {
  ok: true,
  data: T,
} | {
  ok: false,
  error: string,
}

export type Cursor<T> = {
  items: Array<T>,
  hasMore: boolean,
  nextCursorCreatedAt?: string,
  nextCursorId?: string,
}

export type CursorState = {
  id?: string;
  createdAt?: string,
}

export type User = {
  email: string,
  fullName: string,
  roles: string[],
  functionalities: string[],
}

export type RoleMessageType = "user" | "assistant";

export type Chat = {
  id: string,
  title: string,
}

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


