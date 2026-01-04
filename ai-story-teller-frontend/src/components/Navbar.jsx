import React from "react";
import { Book, LogOut, HelpCircle, Pen } from "lucide-react";
import { useContext } from "react";
import { UserContext } from "@/context/UserContext";
import { toast } from "sonner";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const { user, setUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/user/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      if (response.status === 200) {
        setUser(null);
        localStorage.removeItem("user");
        toast.success("Logged out successfully");
        navigate("/auth");
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <nav className="bg-blue-600 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to={"/dashboard"}>
          <div className="flex items-center space-x-2">
            <Book className="text-white" size={24} />
            <span className="text-white text-xl font-bold">AiStoryTeller</span>
          </div>
        </Link>
        <div className="flex items-center space-x-4">
          {user && (
            <a
              href="#previous-assessments" // Change the href to point to the assessments section
              className="text-white hover:text-blue-200 flex items-center text-lg font-semibold"
            >
              <Pen className="mr-1 " size={18} />
              Previous Assessments
            </a>
          )}

          {user && (
            <span className="text-white text-lg font-semibold">
              {user.parentEmail} {/* Displaying the user's email */}
            </span>
          )}

          {user && (
            <button
              className="bg-white text-blue-600 px-4 py-2 rounded-md hover:bg-blue-100 flex items-center"
              onClick={handleLogout}
            >
              <LogOut className="mr-1" size={18} />
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
