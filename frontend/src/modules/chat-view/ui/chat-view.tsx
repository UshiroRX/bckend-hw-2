import React, { useState } from "react";
import axios from "axios";
import { SnakeGame } from "./SnakeGame";

const BOT_START_MESSAGE = {
  sender: "bot",
  text: "Здравствуйте! Введите товар, который вы хотите продать",
};

export const ChatView = () => {
  const [messages, setMessages] = useState([BOT_START_MESSAGE]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [
      ...prev,
      userMessage,
      { sender: "bot", text: "Генерируем..." },
    ]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/create_listing`,
        {
          product: input,
        }
      );
      setMessages((prev) => {
        const msgs = prev.slice(0, -1);
        return [
          ...msgs,
          {
            sender: "bot",
            text:
              res.data.result.generated && res.data.result.translated
                ? res.data.result.generated + "\n" + res.data.result.translated
                : "Нет ответа от сервера.",
          },
        ];
      });
    } catch (e) {
      setMessages((prev) => {
        const msgs = prev.slice(0, -1);
        return [
          ...msgs,
          { sender: "bot", text: "Ошибка соединения с сервером." },
        ];
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-100 to-white">
      <div className="w-full max-w-3xl h-[90vh] flex flex-col border border-black rounded-xl bg-white text-black shadow-lg animate-fade-in overflow-hidden">
        {/* Header */}
        <div className="flex flex-col items-center pt-8 pb-4 px-6 border-b border-gray-200 bg-white z-10">
          <div className="text-5xl mb-2">🤖</div>
          <h1 className="text-2xl font-bold tracking-tight mb-1 text-center">
            AI Product Chat
          </h1>
          <div className="text-gray-500 text-center text-base max-w-md">
            Спросите у ИИ, как лучше описать ваш товар — получите креативное и
            лаконичное описание на русском, казахском и английском!
          </div>
        </div>
        {/* Chat messages (scrollable) */}
        <div className="flex-1 overflow-y-auto px-6 py-6 flex flex-col gap-3">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={
                msg.sender === "user"
                  ? "flex justify-end"
                  : "flex justify-start"
              }
            >
              <span
                className={
                  `inline-block whitespace-pre-line px-4 py-3 rounded-lg max-w-[90%] font-mono text-base border transition-all ` +
                  (msg.sender === "user"
                    ? "bg-gray-100 border-gray-400"
                    : "bg-gray-200 border-gray-300")
                }
              >
                {msg.text}
              </span>
            </div>
          ))}
        </div>
        {/* Input или змейка */}
        <div className="px-6 py-4 border-t border-gray-200 bg-white flex gap-3 z-10 min-h-[64px] items-center justify-center">
          {loading ? (
            <div className="w-full flex justify-center">
              <SnakeGame />
            </div>
          ) : (
            <>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                placeholder="Введите описание товара..."
                className="flex-1 px-4 py-3 rounded-lg border border-black bg-white text-black text-base outline-none disabled:bg-gray-100"
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className={
                  `px-6 py-3 rounded-lg border border-black font-semibold text-base transition ` +
                  (loading || !input.trim()
                    ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                    : "bg-black text-white hover:bg-gray-900 cursor-pointer")
                }
              >
                {loading ? "..." : "Отправить"}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
