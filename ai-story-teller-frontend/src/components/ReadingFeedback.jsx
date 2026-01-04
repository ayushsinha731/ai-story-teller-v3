import React from "react";
import { Sparkles, BookOpen } from "lucide-react";
import ScoreDisplay from "./ScoreDisplay";
import TranscriptDisplay from "./TranscriptDisplay";
import FeedbackSection from "./FeedbackSection";

function ReadingFeedback({
  title,
  transcript,
  transcription,
  score,
  //totalWords,
}) {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      {/* Title Section */}
      <div className="relative bg-gradient-to-r from-purple-100 to-pink-100 rounded-2xl p-8 shadow-lg">
        <Sparkles className="absolute top-4 right-4 text-purple-500 animate-pulse" />
        <h1 className="text-4xl font-bold text-purple-800 mb-2 leading-tight">
          {title}
        </h1>
        <div className="flex items-center gap-2">
          <BookOpen className="text-purple-600 w-5 h-5" />
          <span className="text-purple-600 font-medium">
            Congratulations on completing the story!
          </span>
          
        </div>
      </div>

      <ScoreDisplay score={score} />
      <TranscriptDisplay
        transcript={transcript}
        transcription={transcription}
      />
      <FeedbackSection />
    </div>
  );
}

export default ReadingFeedback;
