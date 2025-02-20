"use client";
import { useState, useEffect } from "react";
import { askQuery } from "./api/query";
import { motion } from "framer-motion";
import { Mic, Send } from "lucide-react";

interface Message {
  query: string;
  response: string;
}

export default function Chatbot() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isListening, setIsListening] = useState(false);

  useEffect(() => {
    let recognition: SpeechRecognition | null = null;

    if (isListening) {
      const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = (event: SpeechRecognitionEvent) => {
          setQuery((prevQuery) => prevQuery + " " + event.results[0][0].transcript);
        };

        recognition.onend = () => setIsListening(false);

        return () => {
          if (recognition) {
            recognition.abort();
          }
        };
      } else {
        console.warn("SpeechRecognition API not supported in this browser.");
        setIsListening(false);
      }
    }
  }, [isListening]);

  const handleSend = async () => {
    if (!query.trim()) return;

    try {
      const result = await askQuery(query);
      setMessages((prev) => [...prev, { query, response: result }]);
      setQuery("");

      const speech = new SpeechSynthesisUtterance(result);
      window.speechSynthesis.speak(speech);
    } catch (error) {
      console.error("Error fetching query:", error);
      setMessages((prev) => [...prev, { query, response: "Error fetching response. Please try again." }]);
      setQuery("");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-5">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1 }} className="text-3xl font-bold mb-4 text-blue-400">
        AI Chatbot
      </motion.h1>
      <div className="w-full max-w-lg p-6 bg-gray-800 rounded-xl shadow-lg flex flex-col">
        <div className="h-48 overflow-y-auto p-3 border border-gray-700 rounded-lg bg-gray-900 text-gray-300">
          {messages.map((msg, index) => (
            <div key={index} className="mb-2">
              <p className="text-blue-300">You: {msg.query}</p>
              <p className="text-gray-300">Bot: {msg.response}</p>
            </div>
          ))}
        </div>
        <div className="flex items-center gap-2 mt-3">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white"
            placeholder="Ask me anything..."
          />
          <button 
            disabled={isListening} 
            onClick={() => setIsListening(true)} 
            className={`p-3 rounded-full ${isListening ? "bg-gray-500" : "bg-red-500 hover:bg-red-600"}`}
          >
            <Mic size={20} />
          </button>
          <button onClick={handleSend} className="bg-blue-500 hover:bg-blue-600 p-3 rounded-full">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
