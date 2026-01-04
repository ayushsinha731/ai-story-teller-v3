// import "./App.css";
import { Route, Routes } from "react-router-dom";
import { useContext } from "react";

import HomePage from "./pages/HomePage";
import AuthPage from "./pages/AuthPage";
import DashboardPage from "./pages/DashboardPage";
import Navbar from "./components/Navbar";
import { UserContext } from "./context/UserContext";
import ReadStoryPage from "./pages/ReadStoryPage";
import AssignmentPage from "./pages/AssignmentPage";
import FeedbackPage from "./pages/FeedbackPage";
import ReadFullStoryPage from "./pages/ReadFullStoryPage";
import FinalFeedback from "./pages/FinalFeedback";

function App() {
  const { user } = useContext(UserContext);

  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/auth" element={user ? <DashboardPage /> : <AuthPage />} />
        <Route
          path="/dashboard"
          element={user ? <DashboardPage /> : <AuthPage />}
        />
        <Route
          path="/dashboard/:sid/ReadStory"
          element={user ? <ReadStoryPage /> : <AuthPage />}
        />
        <Route
          path="/dashboard/:sid/Assessment"
          element={user ? <AssignmentPage /> : <AuthPage />}
        />
        <Route
          path="/dashboard/Feedback/:sid"
          element={user ? <FeedbackPage /> : <AuthPage />}
        />
        <Route
          path="/dashboard/ReadFull/:sid"
          element={user ? <ReadFullStoryPage /> : <AuthPage />}
        />
        <Route
          path="/dashboard/FinalFeedback/:aid"
          element={user ? <FinalFeedback /> : <AuthPage />}
        />
      </Routes>
    </div>
  );
}

export default App;
