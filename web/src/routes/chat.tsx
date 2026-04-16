import { createRoute, redirect } from "@tanstack/react-router"
import { rootRoute } from "./root"
import { useEffect, useRef, useState } from "react";


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

  const [messages, setMessages] = useState<{ role: string; content: string }[]>([])

  const bottomRef = useRef<any>(null);

  // 👇 auto-scroll al último mensaje
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-full min-h-0">

      {/* CONTENEDOR DE MENSAJES */}
      <div className="flex-1 overflow-y-auto flex flex-col justify-end p-4 gap-2">

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[70%] px-4 py-2 rounded-xl
              ${msg.role === "user"
                ? "self-end bg-blue-500 text-white"
                : "self-start bg-gray-200"
              }`}
          >
            {msg.content}
          </div>
        ))}

        {/* 👇 referencia para scroll */}
        <div ref={bottomRef} />
      </div>

      {/* INPUT */}
      <form className="p-2 border-t" action={async (form) => {
        const message = form.get("message")?.toString() || ""
        setMessages(prev => [...prev, { role: "user", content: message }])
      }}>
        <input
          id="message"
          name="message"
          required
          autoFocus
          autoComplete="off"
          className="w-full rounded-2xl border px-4 py-2"
          placeholder="Escribe un mensaje..."
        />
      </form>

    </div>
  );
}

