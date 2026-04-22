import { createRoute, redirect } from "@tanstack/react-router"
import { rootRoute } from "./root"
import { useEffect, useRef, useState } from "react";
import { chatPlain } from "../services/chat.service";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Roles } from "../types";

export const chatRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: ChatPage,
  beforeLoad: ({ context }) => {
    if (!context.user.functionalities.includes('chat')) {
      throw redirect({ to: "/forbidden" });
    }
  }
})

function ChatPage() {
  const [loading, setLoading] = useState(false)
  const [chatId, setChatId] = useState<string | null>(null)
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-full min-h-0 bg-gray-50">

      {/* CONTENEDOR DE MENSAJES */}
      <div className="flex-1 overflow-y-auto p-4 md:p-8">
        <div className="max-w-3xl mx-auto flex flex-col gap-6">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[90%] md:max-w-[80%] px-6 py-4 rounded-2xl shadow-sm ${msg.role === "user"
                  ? "bg-blue-600 text-white shadow-blue-200"
                  : "bg-white text-gray-800 border border-gray-200"
                  }`}
              >
                {msg.role === "user" ? (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  /* Renderizado de Documentación */
                  <div className="prose prose-slate max-w-none prose-p:leading-relaxed prose-pre:bg-gray-800">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          ))}
          {
            loading && (
              <div className="prose prose-slate max-w-none prose-p:leading-relaxed prose-pre:bg-gray-800">
                <div
                  className={`max-w-[90%] md:max-w-[80%] px-6 py-4 rounded-2xl shadow-sm bg-white text-gray-800 border border-gray-200`}
                >
                  Cargando...
                </div>
              </div>
            )
          }
          <div ref={bottomRef} />
        </div>
      </div>

      {/* INPUT */}
      <div className="p-4 bg-white border-t">
        <form
          className="max-w-3xl mx-auto relative"
          action={(form) => {
            const message = form.get("message")?.toString() || "";
            if (!message.trim()) return;

            const inputElement = document.getElementById("message") as HTMLInputElement;
            if (inputElement) inputElement.value = "";

            setMessages((prev) => [...prev, { role: "user", content: message }]);
            setLoading(true);
            chatPlain(message, "gpt-4o-mini", chatId).then(result => {
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
          }}
        >
          <input
            id="message"
            name="message"
            required
            autoFocus
            autoComplete="off"
            className="w-full rounded-xl border border-gray-300 pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
            placeholder="Consulta la documentación interna..."
            defaultValue="Describe la estructura de los comprobantes electrónicos"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-blue-600 hover:bg-blue-50 rounded-full"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}
