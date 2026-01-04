import React from "react";
import { Mic } from "lucide-react";

export default function RecordButton({
  isRecording,
  onRecordStart,
  onRecordEnd,
}) {
  return (
    <button
      onMouseDown={onRecordStart}
      onMouseUp={onRecordEnd}
      onTouchStart={onRecordStart}
      onTouchEnd={onRecordEnd}
      className={`w-full py-4 px-6 rounded-xl text-white font-semibold transition-all transform hover:scale-105 ${
        isRecording
          ? "bg-red-500 animate-pulse"
          : "bg-gradient-to-r from-purple-500 to-blue-500"
      }`}
    >
      <div className="flex items-center justify-center gap-3">
        <Mic size={24} />
        <span>
          {isRecording ? "Recording..." : "Hold to Record Your Answer"}
        </span>
      </div>
    </button>
  );
}
