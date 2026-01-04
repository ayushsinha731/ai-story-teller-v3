import ProgressBar from "@/components/ProgressBar";
import QuestionCard from "@/components/QuestionCard";
import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { MoonLoader } from "react-spinners";
import { ChevronRight } from "lucide-react";

export default function Assessment() {
  const { sid } = useParams();
  const navigate = useNavigate();
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState(Array(5).fill(""));
  const [speechSynthesis, setSpeechSynthesis] = useState(null);
  const [currentAnswer, setCurrentAnswer] = useState("");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `${BACKEND_URL}/api/story/getQuestions/${sid}`,
          {
            method: "GET",
            credentials: "include",
          }
        );
        const data = await response.json();
        console.log("Fetched questions:", data.questions);
        const arrayOfQuestions = data.questions?.map((q) => q.question);
        setQuestions(arrayOfQuestions || []);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching questions:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [sid]);

  useEffect(() => {
    setSpeechSynthesis(window.speechSynthesis);
  }, []);

  const speakText = (text) => {
    if (speechSynthesis) {
      speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      speechSynthesis.speak(utterance);
    }
  };

  useEffect(() => {
    if (currentQuestion >= 0 && questions[currentQuestion]) {
      speakText(questions[currentQuestion]);
      setCurrentAnswer(answers[currentQuestion] || "");
    }
  }, [currentQuestion]);

  const handleAnswerChange = (e) => {
    const newAnswer = e.target.value;
    setCurrentAnswer(newAnswer);
    const newAnswers = [...answers];
    newAnswers[currentQuestion] = newAnswer;
    setAnswers(newAnswers);
    console.log("Updated answer:", newAnswer);
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
    }
  };

  const handleSubmit = async (e) => {
    try {
      setIsSubmitted(true);
      e.preventDefault();
      const response = await fetch(`${BACKEND_URL}/api/story/feedback/${sid}`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ answers }),
      });
      const data = await response.json();
      console.log("Submitted feedback:", data.saveFeedbacks);
      navigate(`/dashboard/Feedback/${sid}`);
    } catch (error) {
      console.error("Error submitting feedback:", error);
    } finally {
      setIsSubmitted(false);
    }
  };

  const canProceed = currentAnswer.trim().split(/\s+/).filter(w => w.length > 0).length >= 5;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 p-6">
      {loading ? (
        <div className="flex justify-center items-center min-h-screen">
          <MoonLoader color="#003ff2" size={90} />
        </div>
      ) : (
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8 transform transition-all">
            <ProgressBar current={currentQuestion} total={questions.length} />

            <QuestionCard
              question={questions[currentQuestion]}
              currentNumber={currentQuestion + 1}
              totalQuestions={questions.length}
              onReadAgain={() => speakText(questions[currentQuestion])}
            />

            <div className="mt-6">

              <textarea
                value={currentAnswer}
                onChange={handleAnswerChange}
                placeholder="Type your answer here... (at least 5 words)"
                className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none min-h-[120px] text-gray-700"
                autoFocus
              />

              {currentAnswer && (
                <div className="mt-2">
                  <p className="text-sm text-gray-600">
                    Word count: {currentAnswer.trim().split(/\s+/).filter(w => w.length > 0).length}
                  </p>
                  {!canProceed && (
                    <p className="text-sm text-red-500 mt-1">
                      Please provide at least 5 words in your answer.
                    </p>
                  )}
                </div>
              )}
            </div>

            <div className="flex justify-end items-center mt-8">
              {currentQuestion === questions.length - 1 ? (
                <button
                  onClick={handleSubmit}
                  disabled={!canProceed || isSubmitted}
                  className={`flex items-center px-6 py-3 rounded-full ${canProceed && !isSubmitted
                    ? "bg-green-500 text-white hover:bg-green-600"
                    : "bg-gray-300 text-gray-500 cursor-not-allowed"
                    } transition duration-300 ease-in-out`}
                >
                  {isSubmitted ? "Submitting..." : "Submit Answers"}
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  disabled={!canProceed}
                  className={`flex items-center px-6 py-3 rounded-full ${canProceed
                    ? "bg-blue-500 text-white hover:bg-blue-600"
                    : "bg-gray-300 text-gray-500 cursor-not-allowed"
                    } transition duration-300 ease-in-out`}
                >
                  Next Question
                  <ChevronRight className="ml-2" size={24} />
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
