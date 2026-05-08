import { Link } from "@tanstack/react-router";
import { useChatHistory } from "../hooks/useChat";

export default function ChatHistory() {

  const { chats, loading, hasMore, loadNext, loadingMore } = useChatHistory()

  return (
    <div className="flex flex-col gap-1 w-full h-full min-h-0">
      <header>Chat History</header>
      <main className="overflow-auto">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <ul className="overflow-y-auto">
            {chats.map((chat) => (
              <li key={chat.id}>
                <Link to="/chat/$chatId" params={{ chatId: chat.id }} className="w-full hover:underline">
                  {chat.title}
                </Link>
              </li>
            ))}
            {
              hasMore && (
                <li>
                  <button className={loadingMore ? "hover:cursor-not-allowed" : "hover:cursor-pointer"} disabled={loadingMore} onClick={loadNext}>Cargar mas</button>
                </li>
              )
            }
          </ul>
        )}
      </main>
    </div>
  )
}
