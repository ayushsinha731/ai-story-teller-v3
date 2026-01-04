import React from "react";
import { Trophy, BookOpen } from "lucide-react";

function FeedbackHeader() {
  return (
    <div className="text-center mb-10">
      <div className="flex justify-center mb-4">
        <Trophy className="w-16 h-16 text-yellow-400" />
      </div>
      <h1 className="text-3xl font-bold text-indigo-600 mb-4">
        Your Reading Adventure Results!
      </h1>
      <div className="bg-white rounded-lg p-6 shadow-md mb-8">
        <BookOpen className="w-8 h-8 text-indigo-500 mx-auto mb-4" />
        <p className="text-gray-600">
          Let's see how well you did on your reading journey! Remember, practice
          makes perfect! 🌟
        </p>
      </div>
    </div>
  );
}

export default FeedbackHeader;
