import { createContext, useState } from "react";
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // State to manage whether the user is in the login or signup mode
  const [authState, setAuthState] = useState("signup"); // Initially set to "signup"

  // Function to toggle between login and signup
  const toggleAuthState = () => {
    setAuthState((prevState) => (prevState === "signup" ? "login" : "signup"));
  };

  return (
    <AuthContext.Provider value={{ authState, toggleAuthState }}>
      {children}
    </AuthContext.Provider>
  );
};
