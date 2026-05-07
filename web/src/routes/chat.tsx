import { createRoute, redirect } from "@tanstack/react-router";
import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import SendIcon from "../components/SendIcon";
import { useStreamChat } from "../hooks/useChat";
import { Roles } from "../types";
import { rootRoute } from "./root";

export const chatRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: ChatPage,
  beforeLoad: ({ context }) => {
    if (!context.auth.hasRole(Roles.NORMAL)) {
      throw redirect({ to: "/forbidden" });
    }
  }
})

function ChatPage() {

  const bottomRef = useRef<HTMLDivElement>(null);
  const {
    loading,
    messages,
    onSubmit,
    value,
    onChangeValue,
  } = useStreamChat()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-full min-h-0 bg-gray-50">

      {/* CONTENEDOR DE MENSAJES */}
      <div className="flex-1 overflow-y-auto p-4 md:p-8">
        <div className="max-w-3xl mx-auto flex flex-col gap-6">
          {messages.map((msg, i) => (msg.role === "user" ? <UserMessage key={i} content={msg.content} /> : <AssistantMessage key={i} content={msg.content} />))}
          {/* {loading && (<LoadingIndicator />)} */}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* INPUT */}
      <div className="p-4 bg-white border-t">
        <form
          className="max-w-3xl mx-auto relative"
          onSubmit={onSubmit}
        >
          <input
            id="message"
            name="message"
            required
            autoFocus
            autoComplete="off"
            disabled={loading}
            className="w-full rounded-xl border border-gray-300 pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
            placeholder="Consulta la documentación interna..."
            value={value}
            onChange={(e) => onChangeValue(e.target.value)}
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-blue-600 hover:bg-blue-50 rounded-full"
          >
            <SendIcon />
          </button>
        </form>
      </div>
    </div>
  );
}

function UserMessage({ content }: { content: string }) {
  return (<div className={`flex justify-end`}>
    <div
      className={`max-w-[90%] md:max-w-[90%] p-4 rounded-2xl shadow-sm bg-blue-600 text-white shadow-blue-200`}
    >
      <p className="whitespace-pre-wrap">{content}</p>
    </div>
  </div>)
}

function AssistantMessage({ content }: { content: string }) {
  return (
    <div className={`flex justify-start`}>
      <div
        className={`max-w-[90%] md:max-w-[90%] p-4 rounded-2xl shadow-sm bg-white text-gray-800 border border-gray-200`}
      >
        <div className="prose prose-slate max-w-none prose-p:leading-relaxed prose-pre:bg-gray-800">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
