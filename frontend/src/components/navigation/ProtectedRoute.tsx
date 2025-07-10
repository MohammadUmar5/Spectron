import type { JSX } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthProvider";

function ProtectedRoute({ element }: { element: JSX.Element }) {
  const { isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }

  return element;
}

export default ProtectedRoute;
