import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthProvider";
import { logout } from "../../services/auth";
import { MenuIcon, X } from "lucide-react";

const links = [
  { id: 1, link: "/about", title: "About" },
  { id: 2, link: "/features", title: "Features" },
  { id: 4, link: "/docs", title: "Docs" },
];

const LogoBox = () => (
  <div className="flex items-center justify-center">
    <Link to="/">
      <img src="/logo.png" alt="logo" className="w-24" />
    </Link>
  </div>
);

const LinkBox = () => (
  <div className="hidden sm:flex items-center justify-center gap-6 ml-24">
    {links.map(({ id, link, title }) => (
      <span
        key={id}
        className="font-bold text-gray-500 text-xl hover:text-black transition-colors duration-200"
      >
        <Link to={link}>{title}</Link>
      </span>
    ))}
  </div>
);

const LoginBtn = () => (
  <>
    <span className="px-4 py-2 rounded-xl">
      <Link to="/login" className="font-bold text-textColor text-xl">
        Log In
      </Link>
    </span>
    <Link to="/signup" className="bg-accentColor px-4 py-2 rounded-xl">
      <p className="text-white font-bold">Sign Up</p>
    </Link>
  </>
);

const NavBar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { isLoggedIn } = useAuth();
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
    <>
      <nav className="w-full h-24 flex items-center justify-between px-4 sm:px-8">
        <LogoBox />
        <LinkBox />

        {/* Desktop Buttons */}
        <div className="hidden sm:flex items-center gap-2 ml-4">
          {isLoggedIn ? (
            <button
              onClick={handleLogout}
              className="bg-accentColor px-4 py-2 rounded-xl"
            >
              <p className="text-white font-bold">Log out</p>
            </button>
          ) : (
            <LoginBtn />
          )}
        </div>

        {/* Mobile Menu Button */}
        <div className="sm:hidden">
          <button onClick={() => setIsMenuOpen(true)}>
            <MenuIcon size={32} color="#1d4640" />
          </button>
        </div>
      </nav>

      {/* Mobile Sidebar Menu */}
      <div
        className={`fixed top-0 right-0 h-full w-full bg-gradient-to-br from-[#f9eee0] via-[#f3e2c7] to-[#e7d4b5] shadow-lg transform transition-transform duration-300 z-50 ${
          isMenuOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between mb-6 pr-6 border-b border-accentColor">
          <LogoBox />
          <button onClick={() => setIsMenuOpen(false)}>
            <X size={28} color="#1d4640" />
          </button>
        </div>
        <div className="flex flex-col px-6 py-4 gap-4">
          {links.map(({ id, link, title }) => (
            <Link
              key={id}
              to={link}
              onClick={() => setIsMenuOpen(false)}
              className="text-gray-700 hover:text-black text-center text-3xl font-semibold"
            >
              {title}
            </Link>
          ))}

          <section className="flex-col w-full py-6 gap-4 text-center bg-white/20 backdrop-blur-lg rounded-2xl shadow-xl mt-8 flex items-center justify-center">
            {!isLoggedIn ? (
              <>
                <Link to="/login" onClick={() => setIsMenuOpen(false)}>
                  <p className="text-textColor text-3xl text-center font-bold">
                    Log In
                  </p>
                </Link>
                <Link
                  to="/signup"
                  className="bg-accentColor px-4 py-2 rounded-xl text-white text-2xl text-center font-bold"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </>
            ) : (
              <button
                onClick={() => {
                  handleLogout();
                  setIsMenuOpen(false);
                }}
                className="bg-accentColor px-4 py-2 rounded-xl text-2xl text-white font-bold"
              >
                Log out
              </button>
            )}
          </section>
        </div>
      </div>
    </>
  );
};

export default NavBar;
