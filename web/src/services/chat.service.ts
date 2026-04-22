import type { Message, Response } from "../types";
import client from "./client";

export const chatPlain = async (message: string, model: string, chatId?: string | null | undefined): Promise<Response<Message>> => {
  try {
    const { data } = await client.post("chat", { message, model, chatId })
    return {
      ok: true,
      data: data.data,
    }
  } catch (error) {
    return {
      ok: false,
      error: ""
    }
  }
}
