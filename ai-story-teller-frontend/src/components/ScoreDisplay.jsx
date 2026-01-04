import React from "react";
import { Trophy } from "lucide-react";

function ScoreDisplay({ score }) {
  const stars = Math.round((score / 100) * 5);

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          <Trophy className="text-yellow-500" />
          Your Reading Score: {score}%
        </h2>
        <div className="flex gap-1">
          {[...Array(5)].map((_, i) => (
            <svg
              key={i}
              className={`w-8 h-8 transition-all ${
                i < stars ? "text-yellow-400 fill-yellow-400" : "text-gray-300"
              } ${i < stars ? "animate-bounce-short" : ""}`}
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
            >
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
            </svg>
          ))}
        </div>
      </div>
      <div className="relative h-4 bg-gray-200 rounded-full overflow-hidden">
        <div
          className="absolute top-0 left-0 h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-1000 ease-out"
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

export default ScoreDisplay;
