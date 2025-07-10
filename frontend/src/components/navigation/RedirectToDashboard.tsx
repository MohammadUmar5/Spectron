// RedirectToDashboard.tsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthProvider";
import { Landing } from "../../pages";

const RedirectToDashboard = () => {
  const { isLoggedIn } = useAuth(); // Assuming this returns null or the logged-in user

  if (isLoggedIn) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Landing />;
};

export default RedirectToDashboard;
