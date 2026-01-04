import React from "react";
import { Volume2 } from "lucide-react";

export default function QuestionCard({
  question,
  currentNumber,
  totalQuestions,
  onReadAgain,
}) {
  return (
    <div className="mb-8">
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
        <p className="text-sm text-yellow-700">
          Remember: Please answer in complete sentences to help improve your
          vocabulary! Single-word answers won't help us understand your
          wonderful ideas.
        </p>
      </div>

      <h2 className="text-2xl font-bold text-gray-800 mb-4">{question}</h2>

      <button
        onClick={onReadAgain}
        className="flex items-center gap-2 px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-600 rounded-full transition-colors"
      >
        <Volume2 size={20} />
        <span>Read Again</span>
      </button>
    </div>
  );
}
