import React from "react";

export default function ProgressBar({ current, total }) {
  const percentage = Math.round(((current + 1) / total) * 100);

  return (
    <div className="mb-8">
      <div className="flex justify-between mb-2">
        <span className="text-sm font-medium text-purple-600">
          Question {current + 1} of {total}
        </span>
        <span className="text-sm font-medium text-purple-600">
          {percentage}%
        </span>
      </div>
      <div className="h-2 bg-purple-100 rounded-full">
        <div
          className="h-2 bg-purple-500 rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
}
