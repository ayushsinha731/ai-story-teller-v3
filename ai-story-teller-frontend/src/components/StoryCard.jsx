import React from "react";
import childImage from "../assets/child-sample.png";
import { FileText } from "lucide-react"; // Importing the lucide-react icon
import { Link, useNavigate } from "react-router-dom";

function StoryCard({ title, description, imageUrl, id, maxPages }) {
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col transition-transform duration-300 hover:scale-105 hover:shadow-lg">
      {imageUrl && (
        <img
          src={imageUrl || ""}
          //alt={title}
          className="w-full h-48 object-cover transition-transform duration-300 hover:scale-110"
        />
      )}
      <div className="p-4 flex flex-col flex-grow">
        <h3 className="text-xl font-semibold mb-2 truncate">{title}</h3>
        <p className="text-gray-600 mb-4 flex-grow">{description}</p>
        <div className="flex items-center text-gray-600 mb-4">
          <FileText className="mr-2" size={20} />
          <span>{maxPages} pages</span>
        </div>
        {/* Buttons section */}
        <div className="flex space-x-4 mt-auto">
          <Link to={`/dashboard/${id}/ReadStory`}>
            <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors duration-300">
              Read
            </button>
          </Link>
          <button
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors duration-300"
            onClick={() => navigate(`/dashboard/${id}/Assessment`)}
          >
            Take Assessment
          </button>
          <Link to={`/dashboard/ReadFull/${id}`}>
            <button className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition-colors duration-300">
              Read Full
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default StoryCard;
