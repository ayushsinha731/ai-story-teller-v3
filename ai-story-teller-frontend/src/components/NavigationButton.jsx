import React from "react";
import { ChevronRight, Award } from "lucide-react";

export default function NavigationButton({
  isLastQuestion,
  canProceed,
  onNext,
  onSubmit,
}) {
  if (isLastQuestion) {
    return (
      <button
        onClick={onSubmit}
        disabled={!canProceed}
        className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all transform hover:scale-105 ${
          canProceed
            ? "bg-gradient-to-r from-yellow-400 to-orange-500 text-white animate-bounce"
            : "bg-gray-200 text-gray-400 cursor-not-allowed"
        }`}
      >
        <Award size={20} />
        Submit Assignment
      </button>
    );
  }

  return (
    <button
      onClick={onNext}
      disabled={!canProceed}
      className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all transform hover:scale-105 ${
        canProceed
          ? "bg-gradient-to-r from-green-500 to-emerald-500 text-white"
          : "bg-gray-200 text-gray-400 cursor-not-allowed"
      }`}
    >
      Next Question
      <ChevronRight size={20} />
    </button>
  );
}
