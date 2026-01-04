import React, { useContext, useEffect, useState } from "react";
import { Plus, X, BookOpen, Upload } from "lucide-react";
import StoryCard from "@/components/StoryCard";
import BookCard from "@/components/BookCard";
import BookUploadModal from "@/components/BookUploadModal";
import { UserContext } from "@/context/UserContext";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

function DashboardPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isBookUploadOpen, setIsBookUploadOpen] = useState(false);
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const [stories, setStories] = useState([]);
  const [books, setBooks] = useState([]);
  const navigate = useNavigate();
  const toggleModal = () => setIsModalOpen(!isModalOpen);
  const [loading, setLoading] = useState(false);
  const { user, setUser } = useContext(UserContext);

  const [storyDetails, setStoryDetails] = useState({
    storyTitle: "",
    storyDescription: "",
    includeImage: false,
    maxPages: 0,
    childAge: user.childAge,
    useBooksContext: false,
    useHistoryContext: false,
  });
  const handleSubmit = async (e) => {
    setLoading(true);
    try {
      e.preventDefault();
      const response = await fetch(`${BACKEND_URL}/api/story/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(storyDetails),
        credentials: "include",
      });
      if (response.status === 201) {
        const data = await response.json();
        const storyId = data.story.id;
        navigate(`/dashboard/${storyId}/ReadStory`);

        console.log(data);
        toggleModal();
      }
    } catch (error) {
      console.error("Error creating story:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchStories = async () => {
      try {
        if (!user?.userId) return;
        const response = await fetch(
          `${BACKEND_URL}/api/story/stories/${user?.userId}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );
        if (response.status === 200) {
          const data = await response.json();
          setStories(data.stories);

          console.log(data);
        }
      } catch (error) {
        console.error("Error fetching stories:", error);
      }
    };

    fetchStories();
  }, [user?.userId, BACKEND_URL]);

  // Fetch user's books
  useEffect(() => {
    const fetchBooks = async () => {
      try {
        if (!user?.userId) return;
        const response = await fetch(`${BACKEND_URL}/api/books`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          setBooks(data.books);
        }
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    };
    fetchBooks();
  }, [user?.userId, BACKEND_URL]);

  const handleBookUploadSuccess = (newBook) => {
    setBooks([newBook, ...books]);
  };

  const handleDeleteBook = async (bookId) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/books/${bookId}`, {
        method: "DELETE",
        credentials: "include",
      });
      if (response.ok) {
        setBooks(books.filter((book) => book.id !== bookId));
      } else {
        alert("Failed to delete book");
      }
    } catch (error) {
      console.error("Error deleting book:", error);
      alert("Error deleting book");
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Story Dashboard</h1>
          <button
            onClick={toggleModal}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center"
          >
            <Plus className="mr-2" size={20} />
            Create New Story
          </button>
        </div>

        {/* My Books Section */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center">
              <BookOpen className="mr-2" size={24} />
              My Books
            </h2>
            <button
              onClick={() => setIsBookUploadOpen(true)}
              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg flex items-center"
            >
              <Upload className="mr-2" size={20} />
              Upload Book
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {books.length === 0 ? (
              <div className="text-lg text-gray-600">
                No books uploaded yet. Upload your first book to personalize story generation!
              </div>
            ) : (
              books.map((book) => (
                <BookCard key={book.id} book={book} onDelete={handleDeleteBook} />
              ))
            )}
          </div>
        </div>

        {/* Stories Section */}
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">My Stories</h2>
        </div>

        {/* Story Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {stories.length === 0 ? (
            <div className="text-lg font-semibold text-gray-600 flex items-center">
              No Stories Found
            </div>
          ) : (
            stories.map((story, index) => (
              <StoryCard
                title={story?.storyTitle}
                description={story?.storyDescription}
                imageUrl={story?.storyContent[0]?.pageImage || ""}
                id={story?.id}
                key={index}
                maxPages={story?.maxPages}
              />
            ))
          )}
          {/* <StoryCard
            title="Galactic Explorers"
            description="Join the crew on an interstellar mission to save humanity."
            imageUrl="https://source.unsplash.com/random/800x600?space"
            id="91011"
          /> */}
        </div>

        {/* Modal */}
        {isModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg p-8 max-w-md w-full">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">Create New Story</h2>
                <button
                  onClick={toggleModal}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X size={24} />
                </button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="mb-4">
                  <label
                    htmlFor="title"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Story Title
                  </label>
                  <input
                    type="text"
                    id="title"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter story title"
                    onChange={(e) =>
                      setStoryDetails({
                        ...storyDetails,
                        storyTitle: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="mb-4">
                  <label
                    htmlFor="description"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Story Description
                  </label>
                  <textarea
                    id="description"
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter story description"
                    onChange={(e) =>
                      setStoryDetails({
                        ...storyDetails,
                        storyDescription: e.target.value,
                      })
                    }
                  ></textarea>
                </div>
                <div className="mb-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      id="includeImage"
                      className="form-checkbox h-5 w-5 text-blue-500"
                      onChange={(e) =>
                        setStoryDetails({
                          ...storyDetails,
                          includeImage: e.target.checked,
                        })
                      }
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      Include Image
                    </span>
                  </label>
                </div>
                <div className="mb-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      id="useBooksContext"
                      className="form-checkbox h-5 w-5 text-green-500"
                      onChange={(e) =>
                        setStoryDetails({
                          ...storyDetails,
                          useBooksContext: e.target.checked,
                        })
                      }
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      Refer Uploaded Books
                    </span>
                  </label>
                  <p className="text-xs text-gray-500 ml-7 mt-1 mb-2">
                    Use your uploaded books for story context
                  </p>

                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      id="useHistoryContext"
                      className="form-checkbox h-5 w-5 text-purple-500"
                      onChange={(e) =>
                        setStoryDetails({
                          ...storyDetails,
                          useHistoryContext: e.target.checked,
                        })
                      }
                    />
                    <span className="ml-2 text-sm text-gray-700">
                      Refer Past Stories
                    </span>
                  </label>
                  <p className="text-xs text-gray-500 ml-7 mt-1">
                    Use your previous stories for context
                  </p>
                </div>
                <div className="mb-6">
                  <label
                    htmlFor="pages"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Maximum Number of Pages
                  </label>
                  <input
                    type="number"
                    id="pages"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter maximum pages"
                    min="1"
                    onChange={(e) =>
                      setStoryDetails({
                        ...storyDetails,
                        maxPages: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    onClick={toggleModal}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
                  >
                    Cancel
                  </button>

                  {loading ? (
                    <Button
                      disabled
                      className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <Loader2 className="animate-spin mr-2 h-4 w-4" />
                      Please wait
                    </Button>
                  ) : (
                    <button
                      type="submit"
                      className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      Generate
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>
        )}
      </div>

      {/* Book Upload Modal */}
      <BookUploadModal
        isOpen={isBookUploadOpen}
        onClose={() => setIsBookUploadOpen(false)}
        onUploadSuccess={handleBookUploadSuccess}
      />
    </div>
  );
}

export default DashboardPage;
