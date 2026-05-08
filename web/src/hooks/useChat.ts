import { useEffect, useState } from "react";
import { chatPlain, chatStream, fetchChatHistory, fetchMessagesByChatId } from "../services/chat.service";
import type { Chat, Message, RoleMessageType } from "../types";
import { useOAuth } from "../providers/oauth.provider";

export function usePlainChat() {
  const [loading, setLoading] = useState(false)
  const [chatId, setChatId] = useState<string | null>(null)
  const [value, setValue] = useState("");
  const [messages, setMessages] = useState<{ role: RoleMessageType; content: string }[]>([]);

  const onSubmit = () => {
    if (!value.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: value }]);
    setLoading(true);
    chatPlain(value, "gpt-4o-mini", chatId).then(result => {
      if (result.ok) {
        setMessages((prev) => [
          ...prev,
          { role: result.data.role, content: result.data.content },
        ]);
        if (!chatId) {
          setChatId(result.data.chatId);
        }
      }
    }).finally(() => { setLoading(false); });
  }

  return {
    loading,
    chatId,
    value,
    messages,
    onSubmit,
    onChangeValue: (v: string) => setValue(v),
  }
}

export function useStreamChat(_chatId: number | string | undefined) {
  const { token } = useOAuth()

  const [isStreaming, setIsStreaming] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [chatId, setChatId] = useState<string | number | null | undefined>(_chatId)
  const [value, setValue] = useState("");
  const [messages, setMessages] = useState<{ role: RoleMessageType; content: string }[]>([]);

  const onSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!value.trim()) return;

    const messageToSend = value + "";
    setValue("");

    setMessages((prev) => [...prev, { role: "user", content: messageToSend }]);
    setIsStreaming(true);

    try {
      let assistantContent = "";

      for await (const event of chatStream(messageToSend, "gpt-4o-mini", chatId, token)) {

        // Accumulate the content from stream events
        if (event.type == "chunk") {
          assistantContent += event.data;

          // Update message in real-time
          setMessages((prev) => {
            const updated = [...prev];
            if (updated[updated.length - 1]?.role === "assistant") {
              updated[updated.length - 1].content = assistantContent;
            } else {
              updated.push({ role: "assistant", content: assistantContent });
            }
            return updated;
          });
        } else if (event.type === "start") {
          // Capture chatId from first event if not set
          if (!chatId && event.data.chat_id) {
            setChatId(event.data.chat_id);
          }
        }
      }
    } catch (error) {
      console.error("Stream error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error processing response" },
      ]);
    } finally {
      setIsStreaming(false);
    }
  };

  const fetchMessages = async (chatId: string | number) => {
    setLoadingMessages(true);
    const result = await fetchMessagesByChatId(chatId);
    if (result.ok) {
      setMessages(result.data.map(msg => ({ role: msg.role, content: msg.content })));
    }
    setLoadingMessages(false);
  }

  useEffect(() => {
    if (!_chatId) return;
    fetchMessages(_chatId);
  }, [_chatId]);

  return {
    isStreaming,
    loadingMessages,
    chatId,
    messages,
    onSubmit,
    //
    value,
    onChangeValue: (v: string) => setValue(v),
  }
}

export function useChatHistory() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    const result = await fetchChatHistory();
    if (result.ok) {
      setChats(result.data);
    }
    setLoading(false);
  }

  useEffect(() => {
    fetchData();
  }, []);

  return {
    chats,
    loading,
  }
}
