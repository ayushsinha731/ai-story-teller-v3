import React, { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, ClipboardCheck } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

function ReadStoryPage() {
  const [currentPage, setCurrentPage] = useState(0); // Current page number
  const [story, setStory] = useState(null); // Story data
  const { sid } = useParams(); // Story ID from URL params
  const navigate = useNavigate();
  // Fetch the story when the component mounts or when `sid` changes
  useEffect(() => {
    const fetchStory = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/story/getStory/${sid}`, {
          credentials: "include", // Ensure cookies are sent with the request
        });
        if (res.status === 200) {
          const data = await res.json();
          setStory(data.story);
          console.log(data.story); // Debug: log story data
        } else {
          console.error("Failed to fetch story: ", res.statusText);
        }
      } catch (error) {
        console.error("Error fetching story:", error);
      }
    };

    fetchStory(); // Call the async function inside useEffect
  }, [sid]); // Dependency array ensures the effect runs when `sid` changes

  const handlePrevious = () => {
    setCurrentPage((prev) => Math.max(0, prev - 1));
  };

  const handleNext = () => {
    if (story) {
      setCurrentPage((prev) =>
        Math.min(story.storyContent.length - 1, prev + 1)
      );
    }
  };

  const handleAssessment = () => {
    console.log("Taking assessment");
    navigate(`/dashboard/${sid}/Assessment`);
  };

  if (!story) {
    return <div>Loading story...</div>;
  }

  const progress = ((currentPage + 1) / story.storyContent.length) * 100;

  return (
    <div className="max-w-3xl mx-auto p-8 bg-white rounded-lg shadow-lg">
      <div className="mb-6 h-2 bg-gray-200 rounded-full">
        <div
          className="h-2 bg-blue-500 rounded-full transition-all duration-300 ease-in-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      {/* Show story title and author on the first page */}
      {currentPage === 0 && (
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {story.storyTitle}
          </h1>
          <h2 className="text-lg text-gray-600">by {story.storyAuthor}</h2>
        </div>
      )}

      <div className="mb-8">
        <p className="text-gray-700 leading-relaxed text-lg">
          {currentPage === 0 ? (
            <>
              <span className="text-6xl font-bold float-left mr-3 mt-1">
                {story.storyContent[currentPage].pageText.charAt(0)}
              </span>
              {story.storyContent[currentPage].pageText.slice(1)}
            </>
          ) : (
            story.storyContent[currentPage].pageText
          )}
        </p>
      </div>

      {story.storyContent[currentPage].pageImage && (
        <div className="mb-8">
          <img
            src={story.storyContent[currentPage].pageImage}
            alt={`Story illustration ${currentPage + 1}`}
            className="w-full aspect-video object-cover rounded-lg shadow-md"
          />
        </div>
      )}

      <div className="flex justify-between items-center">
        <button
          onClick={handlePrevious}
          disabled={currentPage === 0}
          className={`flex items-center px-6 py-3 rounded-full ${currentPage === 0
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-blue-500 text-white hover:bg-blue-600"
            } transition duration-300 ease-in-out`}
        >
          <ChevronLeft className="mr-2" size={24} />
          Previous
        </button>
        {currentPage === story.storyContent.length - 1 ? (
          <button
            onClick={handleAssessment}
            className="flex items-center px-6 py-3 rounded-full bg-green-500 text-white hover:bg-green-600 transition duration-300 ease-in-out"
          >
            <ClipboardCheck className="mr-2" size={24} />
            Take Assessment
          </button>
        ) : (
          <button
            onClick={handleNext}
            disabled={currentPage === story.storyContent.length - 1}
            className={`flex items-center px-6 py-3 rounded-full ${currentPage === story.storyContent.length - 1
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-blue-500 text-white hover:bg-blue-600"
              } transition duration-300 ease-in-out`}
          >
            Next
            <ChevronRight className="ml-2" size={24} />
          </button>
        )}
      </div>
    </div>
  );
}

export default ReadStoryPage;
