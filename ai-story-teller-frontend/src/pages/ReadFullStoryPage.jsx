import React, { useState, useEffect } from "react";
import axios from "axios";
import { Mic, MicOff, Upload, LineChart, Volume2 } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";

const ReadFullStoryPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioList, setAudioList] = useState([]);
  const [story, setStory] = useState("");
  const { sid } = useParams();
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const [loading, setLoading] = useState(false);
  const [aid, setAid] = useState();
  const [isLoaded, setIsLoaded] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const getStory = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `${BACKEND_URL}/api/story/getFullStory/${sid}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );
        const data = await response.json();
        setStory(data.wholeStory);
        console.log(data);
      } catch (error) {
        console.error("Error fetching story:", error);
      } finally {
        setLoading(false);
      }
    };
    getStory();
  }, [sid]);

  /*  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/audios`)
      .then((response) => setAudioList(response.data))
      .catch((error) => console.error("Error fetching audio list:", error));
  }, []); */

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (e) => {
      setAudioBlob(e.data);
    };
    recorder.start();
    setMediaRecorder(recorder);
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorder.stop();
    setIsRecording(false);
  };

  const uploadAudio = async () => {
    const formData = new FormData();
    formData.append(
      "audio",
      new Blob([audioBlob], { type: "audio/wav" }),
      "recording.wav"
    );

    try {
      setIsLoaded(true);
      const response = await fetch(`${BACKEND_URL}/upload/${sid}`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });
      if (response.status === 201) {
        console.log("Audio uploaded successfully");
        const data = await response.json();
        setAid(data);
        //console.log("Data is ", aid);
      }
      alert("Audio uploaded successfully");
      //window.location.reload();
    } catch (error) {
      console.error("Error uploading audio:", error);
    } finally {
      setIsLoaded(false);
    }
  };
  useEffect(() => {
    if (aid) {
      console.log("Updated aid:", aid);
    }
  }, [aid]);

  // const viewResults = async () => {
  //   const res = await fetch(`http://127.0.0.1:8000/process-audio/${aid}`, {
  //     method: "GET",
  //   });
  //   const data = await res.json();
  //   console.log(data);
  // };
  const viewResults = async () => {
    if (!aid) {
      console.error("Error: aid is undefined");
      return;
    }
    try {
      const res = await fetch(`${BACKEND_URL}/process-audio/${aid}`, {
        method: "GET",
        credentials: "include",
      });
      const data = await res.json();
      console.log(data);
      navigate(`/dashboard/FinalFeedback/${aid}`);
    } catch (error) {
      console.error("Error fetching results:", error);
    }
  };

  /* const story = `
    Once upon a time, in a lush green forest, there lived a curious little rabbit named Benny. Benny loved to explore his surroundings and make new friends. One sunny day, he decided to venture beyond the familiar trees and bushes he knew so well.

    As he hopped along, he encountered a wise old tortoise who shared tales of distant lands and adventures. Inspired, Benny set off on a quest to discover the world beyond his home. Through challenges and friendships, he learned valuable lessons about courage and kindness, reminding us all that adventure awaits those who seek it.
  `; */

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-indigo-900 to-purple-900">
      <div className="flex-1 p-8 flex flex-col justify-center items-center">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 w-full max-w-md">
          <div className="flex items-center gap-3 mb-8">
            <Volume2 className="w-8 h-8 text-purple-300" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-200 to-pink-200 bg-clip-text text-transparent">
              Audio Recorder
            </h1>
          </div>

          <div className="space-y-6">
            <div className="flex justify-center">
              <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 ${isRecording
                  ? "bg-red-500 hover:bg-red-600 animate-pulse"
                  : "bg-purple-500 hover:bg-purple-600"
                  }`}
              >
                {isRecording ? (
                  <MicOff className="w-10 h-10 text-white" />
                ) : (
                  <Mic className="w-10 h-10 text-white" />
                )}
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Button
                onClick={uploadAudio}
                disabled={!audioBlob}
                className={`flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${audioBlob
                  ? "bg-emerald-500 hover:bg-emerald-600 text-white"
                  : "bg-gray-400 cursor-not-allowed text-gray-200"
                  }`}
              >
                <Upload className="w-5 h-5" />
                Upload
              </Button>

              <Button
                onClick={viewResults}
                disabled={isLoaded}
                className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-white font-medium transition-all duration-300"
              >
                <LineChart className="w-5 h-5" />
                Results
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 bg-white">
        <div className="h-full p-8 overflow-y-auto">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">Story</h2>
          <div className="prose prose-xl max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-line text-xl font-medium">
              {story}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReadFullStoryPage;
