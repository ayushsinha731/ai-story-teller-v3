import React from "react";
import { Star } from "lucide-react";

export default function FeedbackCard({ data, index }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg border-2 border-indigo-100 hover:border-indigo-200 transition-all">
      <div className="flex items-start gap-4">
        <div className="bg-indigo-100 rounded-full p-3">
          <Star className="w-6 h-6 text-indigo-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-indigo-600 mb-4">
            Question {index + 1}
          </h3>

          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">
                Original Question:
              </h4>
              <p className="bg-purple-50 rounded-lg p-3 text-gray-600">
                {data?.question}
              </p>
            </div>

            <div>
              <h4 className="font-medium text-gray-700 mb-2">
                Correct Answer:
              </h4>
              <p className="bg-green-50 rounded-lg p-3 text-gray-600">
                {data?.answer}
              </p>
            </div>

            <div>
              <h4 className="font-medium text-gray-700 mb-2">Your Reading:</h4>
              <p className="bg-blue-50 rounded-lg p-3 text-gray-600">
                {data?.userAnswer}
              </p>
            </div>

            <div>
              <h4 className="font-medium text-gray-700 mb-2">
                Friendly Feedback:
              </h4>
              <p className="bg-yellow-50 rounded-lg p-3 text-gray-600">
                {data?.feedback}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <span className="font-medium text-gray-700">Star Rating:</span>
              <div className="flex gap-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    className={`w-5 h-5 ${i < data?.rating
                        ? "text-yellow-400 fill-yellow-400"
                        : "text-gray-200"
                      }`}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
