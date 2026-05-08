import { createRoute, redirect } from "@tanstack/react-router";
import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
// import SendIcon from "../components/SendIcon";
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

  return (
    <Chat chatId={undefined} />
  )
}

export function Chat({ chatId }: { chatId: number | string | undefined }) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const {
    isStreaming,
    loadingMessages,
    messages,
    onSubmit,
    value,
    onChangeValue,
  } = useStreamChat(chatId)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (loadingMessages) return <ChatSkeleton />;

  return (
    <div className="flex flex-col h-full min-h-0 bg-gray-50 text-gray-900">

      {/* AREA DE MENSAJES */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden custom-scrollbar">
        <div className="max-w-3xl mx-auto p-4 md:p-8 flex flex-col gap-6">

          {messages.length === 0 && !isStreaming && (
            <div className="flex flex-col items-center justify-center h-64 text-center">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-4">
                <MessageIcon size={32} />
              </div>
              <h3 className="text-lg font-medium text-gray-700">¿En qué puedo ayudarte hoy?</h3>
              <p className="text-gray-500 text-sm">Consulta la documentación interna del proyecto.</p>
            </div>
          )}

          {messages.map((msg, i) => (
            msg.role === "user"
              ? <UserMessage key={i} content={msg.content} />
              : <AssistantMessage key={i} content={msg.content} />
          ))}

          {/* Indicador de carga de streaming */}
          {isStreaming && messages[messages.length - 1]?.role === 'user' && (
            <div className="flex justify-start">
              <div className="bg-white p-4 rounded-2xl border border-gray-200">
                <span className="flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]" />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]" />
                </span>
              </div>
            </div>
          )}

          <div ref={bottomRef} className="h-4" />
        </div>
      </div>

      {/* INPUT CONTAINER */}
      <div className="p-4 bg-white border-t border-gray-200 shadow-[0_-4px_12px_rgba(0,0,0,0.02)]">
        <form
          className="max-w-3xl mx-auto relative group"
          onSubmit={(e) => {
            e.preventDefault();
            if (!value.trim() || isStreaming) return;
            onSubmit(e);
          }}
        >
          <input
            id="message"
            name="message"
            required
            autoFocus
            autoComplete="off"
            disabled={isStreaming}
            className="w-full rounded-xl border border-gray-300 pl-4 pr-14 py-4
                     focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                     shadow-sm transition-all disabled:bg-gray-50 disabled:text-gray-500"
            placeholder="Escribe tu pregunta aquí..."
            value={value}
            onChange={(e) => onChangeValue(e.target.value)}
          />
          <button
            type="submit"
            disabled={isStreaming || !value.trim()}
            className={`absolute right-2 top-1/2 -translate-y-1/2 p-2.5 rounded-lg transition-all
              ${isStreaming || !value.trim()
                ? 'text-gray-300 cursor-not-allowed'
                : 'text-white bg-blue-600 hover:bg-blue-700 shadow-md active:scale-95'
              }`}
          >
            {isStreaming ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <SendIcon size={20} />
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

const ChatSkeleton = () => (
  <div className="flex flex-col h-full bg-gray-50 animate-pulse">
    <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
      <div className="max-w-3xl mx-auto w-full">
        <div className="flex flex-col items-end mb-6"><div className="w-3/4 h-20 bg-gray-200 rounded-2xl rounded-tr-none" /></div>
        <div className="flex flex-col items-start mb-6"><div className="w-full h-32 bg-gray-300 rounded-2xl rounded-tl-none" /></div>
        <div className="flex flex-col items-end"><div className="w-1/2 h-12 bg-gray-200 rounded-2xl rounded-tr-none" /></div>
      </div>
    </div>
    <div className="p-4 bg-white border-t">
      <div className="max-w-3xl mx-auto h-12 bg-gray-100 rounded-xl" />
    </div>
  </div>
);

function UserMessage({ content }: { content: string }) {
  return (<div className="flex justify-end w-full">
    <div className="max-w-[85%] md:max-w-[75%] p-4 rounded-2xl shadow-sm bg-blue-600 text-white rounded-tr-none">
      <p className="whitespace-pre-wrap text-sm md:text-base">{content}</p>
    </div>
  </div>)
}

function AssistantMessage({ content }: { content: string }) {
  return (
    <div className="flex justify-start w-full">
      <div className="max-w-[90%] md:max-w-[85%] p-4 rounded-2xl shadow-sm bg-white text-gray-800 border border-gray-200 rounded-tl-none">
        <div className="prose prose-sm md:prose-base prose-slate max-w-none
          prose-p:leading-relaxed prose-pre:bg-gray-900 prose-pre:text-gray-100 prose-code:text-blue-600 prose-code:bg-blue-50 prose-code:px-1 prose-code:rounded">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}

const MessageIcon = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg>
);
// Iconos sugeridos (puedes usar Lucide-react o tus SVGs)
const SendIcon = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="m22 2-7 20-4-9-9-4Z" /><path d="M22 2 11 13" /></svg>
);
