import React, { useContext } from "react";
import SignUpForm from "@/components/ui/auth/SignUpForm";
import { AuthContext } from "@/context/AuthContext";
import LoginForm from "@/components/ui/auth/LoginForm";

function AuthPage() {
  const { authState, toggleAuthState } = useContext(AuthContext);
  return <div>{authState === "signup" ? <SignUpForm /> : <LoginForm />}</div>;
}

export default AuthPage;
