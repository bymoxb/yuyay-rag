import type { Chat, Message, Response } from "../types";
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

export async function* chatStream(message: string, model: string, chatId: string | number | null | undefined, token: string): AsyncGenerator<any, void, unknown> {
  const url = `${client.defaults.baseURL}/stream`;
  const headers: any = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify({ message, model, chat_id: chatId }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Response body is not readable');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6).trim();
          if (dataStr) {
            try {
              const event = JSON.parse(dataStr);
              yield event;
            } catch (parseError) {
              console.error('Failed to parse SSE data:', parseError);
            }
          }
        }
      }
    }
  } catch (error) {
    console.error('Error in chatStream:', error);
    throw error;
  }
}

export const fetchChatHistory = async (): Promise<Response<Chat[]>> => {
  try {
    const { data } = await client.get("chat")
    return {
      ok: true,
      data: data.data,
    }
  } catch (error) {
    return { ok: false, error: "Failed to fetch chat history" }
  }
}

export const fetchMessagesByChatId = async (chatId: string | number): Promise<Response<Message[]>> => {
  try {
    const { data } = await client.get(`chat/${chatId}/messages`)
    return {
      ok: true,
      data: data.data,
    }
  } catch (error) {
    return {
      ok: false,
      error: "Failed to fetch messages for chat"
    }
  }
}
