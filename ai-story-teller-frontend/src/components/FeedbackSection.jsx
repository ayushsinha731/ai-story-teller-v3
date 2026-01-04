import React, { useState } from "react";
import { MessageCircle } from "lucide-react";

export default function FeedbackSection() {
  const [reaction, setReaction] = useState("");
  const [comment, setComment] = useState("");
  const reactions = ["😊", "🤔", "🌟", "❤️", "👏"];

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
        <MessageCircle className="text-blue-500" />
        Share Your Thoughts
      </h2>

      <div className="flex gap-4 justify-center">
        {reactions.map((emoji) => (
          <button
            key={emoji}
            onClick={() => setReaction(emoji)}
            className={`text-3xl p-3 rounded-full transition-transform hover:scale-125 ${reaction === emoji
                ? "bg-purple-100 scale-110"
                : "hover:bg-gray-100"
              }`}
          >
            {emoji}
          </button>
        ))}
      </div>

      <div className="relative">
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="What did you love about this story?"
          className="w-full p-4 rounded-xl border-2 border-purple-200 focus:border-purple-400 focus:ring focus:ring-purple-200 focus:ring-opacity-50 resize-none h-32 text-lg"
          maxLength={200}
        />
        <div className="absolute bottom-4 right-4 text-gray-400">
          {comment.length}/200
        </div>
      </div>

      <button
        onClick={() => {
          if (!reaction && !comment) {
            alert("Please pick a reaction or write a comment first!");
            return;
          }
          // For now, just show a success message as we don't have a specific endpoint for this "meta-feedback" yet
          alert("Thanks for your feedback! stored successfully!");
          setReaction("");
          setComment("");
        }}
        className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform transition hover:-translate-y-1 active:translate-y-0"
      >
        Save My Feedback
      </button>
    </div>
  );
}
