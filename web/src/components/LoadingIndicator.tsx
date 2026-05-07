import TypingIndicator from "./TypingIndicator";

export default function LoadingIndicator() {
  return (
    <div className="prose prose-slate max-w-none prose-p:leading-relaxed prose-pre:bg-gray-800">
      <div
        className={`max-w-[90%] md:max-w-[80%] px-6 py-4 rounded-2xl shadow-sm bg-white text-gray-800 border border-gray-200`}
      >
        <TypingIndicator />
      </div>
    </div>
  )
}
