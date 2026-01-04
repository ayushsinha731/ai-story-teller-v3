import React, { useEffect, useState } from "react";
import FeedbackCard from "../components/FeedbackCard";
import FeedbackHeader from "../components/FeedbackHeader";
import { useParams } from "react-router-dom";
import { MoonLoader } from "react-spinners";

const sampleQuestions = [
  {
    id: 1,
    question: "The cat sat on the mat.",
    correctAnswer: "The cat sat on the mat.",
    userAnswer: "The cat sat on the mat.",
    feedback:
      "Excellent pronunciation! You read all words clearly and accurately.",
    rating: 9,
  },
  {
    id: 2,
    question: "Sally sells seashells by the seashore.",
    correctAnswer: "Sally sells seashells by the seashore.",
    userAnswer: "Sally sells shells by the seashore.",
    feedback:
      "Good effort! Watch out for the word 'seashells' - try breaking it down: sea-shells.",
    rating: 7,
  },
];

function FeedbackPage() {
  const { sid } = useParams();
  const [loading, setLoading] = useState(true);
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const [feedback, setFeedback] = useState([]);

  useEffect(() => {
    // Fetch feedback from the backend
    const fetchFeedback = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `${BACKEND_URL}/api/story/getFeedback/${sid}`,
          {
            method: "GET",
            credentials: "include",
          }
        );
        const data = await response.json();
        console.log("Fetched feedback:", data?.feedback.feedbacks);
        setFeedback(data?.feedback.feedbacks || []);
      } catch (error) {
        console.error("Error fetching feedback:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchFeedback();
  }, [sid]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <FeedbackHeader />

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <MoonLoader color="#4a90e2" size={60} />
          </div>
        ) : (
          <div className="space-y-8">
            {feedback.map((data, index) => (
              <FeedbackCard key={index} data={data} index={index} />
            ))}
          </div>
        )}

        <div className="mt-8 bg-white rounded-lg p-6 shadow-md border-2 border-indigo-100">
          <p className="text-gray-600 text-center">
            Keep practicing and you'll become an amazing reader! Every word you
            read makes you stronger! 🌈 📚
          </p>
        </div>
      </div>
    </div>
  );
}

export default FeedbackPage;
