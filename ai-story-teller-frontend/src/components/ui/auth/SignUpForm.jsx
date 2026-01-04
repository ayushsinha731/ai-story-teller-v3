import React, { useContext, useState } from "react";
import {
  User,
  Mail,
  UserCircle,
  Calendar,
  GraduationCap,
  Lock,
} from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "@/context/AuthContext";
import { toast } from "sonner";
import { Button } from "../button";
import { Loader2 } from "lucide-react";
import { UserContext } from "@/context/UserContext";

function SignUpForm() {
  const navigate = useNavigate();
  const [signUpInfo, setSignUpInfo] = useState({
    parentName: "",
    parentEmail: "",
    childName: "",
    childAge: "",
    childStandard: "",
    password: "",
  });
  const [loading, setLoading] = useState(false);
  const { user, setUser } = useContext(UserContext);
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    // Client-side validation
    if (signUpInfo.password.length < 8) {
      toast.error("Password must be at least 8 characters long");
      return;
    }

    const age = parseInt(signUpInfo.childAge);
    if (isNaN(age) || age < 5 || age > 15) {
      toast.error("Child age must be between 5 and 15");
      return;
    }

    const standard = parseInt(signUpInfo.childStandard);
    if (isNaN(standard) || standard < 1 || standard > 8) {
      toast.error("Standard must be between 1 and 8");
      return;
    }

    try {
      setLoading(true);
      console.log(signUpInfo);
      const response = await fetch(`${BACKEND_URL}/api/user/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signUpInfo),
        credentials: "include",
      });
      const data = await response.json();
      if (!response.ok) {
        // Handle non-200 responses specifically
        if (data.details) {
          // Flatten validation errors if present
          const errors = Object.values(data.details).join(", ");
          toast.error(errors || data.error || "Signup failed");
        } else {
          toast.error(data.error || "Signup failed");
        }
        return;
      }

      setUser(data);
      localStorage.setItem("user", JSON.stringify(data));

      navigate("/dashboard");
      toast.success(data.message);
    } catch (error) {
      console.error(error);
      toast.error("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  const { authState, toggleAuthState } = useContext(AuthContext);

  return (
    <div className="max-w-md w-full bg-white shadow-md rounded-lg p-8 mx-auto my-[80px]">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
        Sign Up
      </h2>
      <form className="space-y-4" onSubmit={handleFormSubmit}>
        {/* Parent Name Field */}
        <div>
          <label
            htmlFor="parentName"
            className="block text-sm font-medium text-gray-700"
          >
            Parent Name
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              id="parentName"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
              placeholder="John Doe"
              onChange={(e) =>
                setSignUpInfo({ ...signUpInfo, parentName: e.target.value })
              }
            />
          </div>
        </div>

        {/* Parent Email Field */}
        <div>
          <label
            htmlFor="parentEmail"
            className="block text-sm font-medium text-gray-700"
          >
            Parent Email
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="email"
              id="parentEmail"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
              placeholder="john@example.com"
              onChange={(e) =>
                setSignUpInfo({ ...signUpInfo, parentEmail: e.target.value })
              }
            />
          </div>
        </div>

        {/* Child Name Field */}
        <div>
          <label
            htmlFor="childName"
            className="block text-sm font-medium text-gray-700"
          >
            Child Name
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <UserCircle className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              id="childName"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
              placeholder="Jane Doe"
              onChange={(e) =>
                setSignUpInfo({ ...signUpInfo, childName: e.target.value })
              }
            />
          </div>
        </div>

        {/* Child Age Field */}
        <div>
          <label
            htmlFor="childAge"
            className="block text-sm font-medium text-gray-700"
          >
            Child Age
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Calendar className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="number"
              id="childAge"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
              placeholder="10"
              onChange={(e) =>
                setSignUpInfo({ ...signUpInfo, childAge: e.target.value })
              }
            />
          </div>
        </div>

        {/* Child Standard Field */}
        <div>
          <label
            htmlFor="childStandard"
            className="block text-sm font-medium text-gray-700"
          >
            Child Standard
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <GraduationCap className="h-5 w-5 text-gray-400" />
            </div>
            <select
              id="childStandard"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
              onChange={(e) =>
                setSignUpInfo({ ...signUpInfo, childStandard: e.target.value })
              }
            >
              <option value="">Select grade</option>
              <option value="1">1st Grade</option>
              <option value="2">2nd Grade</option>
              <option value="3">3rd Grade</option>
              <option value="4">4th Grade</option>
              <option value="5">5th Grade</option>
            </select>
          </div>
        </div>

        {/* Password Field */}
        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="password"
              id="password"
              className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
              placeholder="••••••••"
              onChange={(e) =>
                setSignUpInfo({ ...signUpInfo, password: e.target.value })
              }
            />
          </div>
        </div>

        {/* Submit Button */}
        <div>
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
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign Up
            </button>
          )}
        </div>

        {/* Link to Login */}
        <div className="text-sm text-center">
          Already have an account?{" "}
          <Link
            to="/auth"
            className="text-indigo-600 hover:text-indigo-500 font-medium"
            onClick={() => toggleAuthState()}
          >
            Log in
          </Link>
        </div>
      </form>
    </div>
  );
}

export default SignUpForm;
