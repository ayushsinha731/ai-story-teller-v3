import React from "react";
import { diffWords } from "diff";

function TranscriptDisplay({ transcript ="", transcription="" }) {
  ////////////////////
  const getOriginalHighlightedText = (original, reading) => {
    const diff = diffWords(original, reading); // Compare texts

    return diff.map((part, index) => {
      if (part.removed) {
        // Highlight missing words in the Original Text
        return (
          <span key={index} className="bg-red-200 text-red-700 px-1 rounded">
            {part.value} {/* Original word is missing in the reading */}
          </span>
        );
      } else if (part.added) {
        // If there are added words in the reading, don't display them in the Original
        return null;
      } else {
        // No change, display as regular text (from the original text)
        return part.value;
      }
    });
  };

  // Function to generate highlighted text for the Your Reading Text
  const getReadingHighlightedText = (original, reading) => {
    const diff = diffWords(original, reading); // Compare texts

    return diff.map((part, index) => {
      if (part.added) {
        // Highlight extra words in the Your Reading
        return (
          <span key={index} className="bg-green-200 text-green-700 px-1 rounded">
            {part.value} {/* Extra word in the reading */}
          </span>
        );
      } else if (part.removed) {
        // If there are missing words in the reading, don't display them in the Your Reading
        return null;
      } else {
        // No change, display as regular text (from the reading text)
        return part.value;
      }
    });
  };
  ///////////////////
  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg space-y-6">
      <div className="space-y-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Original Text
          </h2>
          <p className="text-lg leading-relaxed text-gray-700 font-medium bg-purple-50 p-4 rounded-xl">
            {/* {transcript} */}
            {getOriginalHighlightedText(transcript, transcription)}
          </p>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Your Reading
          </h2>
          <p className="text-lg leading-relaxed text-gray-700 font-medium bg-gray-50 p-4 rounded-xl">
            {/* {transcription} */}
            {getReadingHighlightedText(transcript, transcription)}
          </p>
        </div>
      </div>
    </div>
  );
}

export default TranscriptDisplay;
