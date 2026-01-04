import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { BrowserRouter as Router } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext.jsx";
import { Toaster } from "sonner";
import { UserProvider } from "./context/UserContext.jsx";
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Router>
      <AuthProvider>
        <UserProvider>
          <App />
          <Toaster />
        </UserProvider>
      </AuthProvider>
    </Router>
  </StrictMode>
);
