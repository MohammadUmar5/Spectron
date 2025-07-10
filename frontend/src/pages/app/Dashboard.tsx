import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthProvider";
import { logout } from "../../services/auth";

const Dashboard = () => {
  const { isLoggedIn, hasProfile } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate("/login");
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };
  return (
    <section className="w-screen min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-[#f9eee0] via-[#f3e2c7] to-[#e7d4b5]">
      <h1 className="text-7xl font-bold mb-6 text-textColor">Dashboard</h1>
      <p className="text-xl font-bold text-textColor">
        {isLoggedIn ? "You are logged in" : "You are not logged in"}
      </p>
      <p className="text-xl font-bold text-textColor">
        {hasProfile ? "You have a profile" : "You do not have a profile"}
      </p>
      <button
        onClick={handleLogout}
        className="mt-6 px-6 py-2 bg-red-500 text-white font-semibold rounded-lg shadow hover:bg-red-600 transition cursor-pointer"
      >
        Log Out
      </button>
    </section>
  );
};

export default Dashboard;
