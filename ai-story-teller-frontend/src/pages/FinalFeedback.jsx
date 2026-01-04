import React, { useEffect } from "react";
import ReadingFeedback from "@/components/ReadingFeedback";
import { useParams } from "react-router-dom";
import { useState } from "react";

function FinalFeedback() {
  const { aid } = useParams();
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const [audio, setAudio] = useState();
  useEffect(() => {
    const getFeedback = async () => {
      try {
        const response = await fetch(
          `${BACKEND_URL}/audio/finalFeedback/${aid}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );
        const data = await response.json();
        console.log(data);
        setAudio(data);
      } catch (error) {
        console.error("Error fetching feedback:", error);
      }
    };
    getFeedback();
  }, [aid]);
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-pink-50 py-12">
      <ReadingFeedback
        title={audio?.story.storyTitle}
        transcription={audio?.audio.transcript}
        transcript={audio?.audio.wholeStory}
        score={Math.round(audio?.audio.score)}
      //totalWords={150}
      />
    </div>
  );
}

export default FinalFeedback;
