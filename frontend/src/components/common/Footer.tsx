import { Link } from "react-router-dom";
import { FaGithub, FaLinkedin, FaYoutube } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="w-full mt-12 border-t-2 border-t-[#e5c798] shadow-inner shadow-[#e5c798] bg-[#ebd8ba]">
      <div className="w-full flex flex-col md:flex-row px-12 py-10 gap-8">
        {/* Left - About Spectron */}
        <div className="md:w-1/3 flex flex-col items-start justify-center space-y-4">
          <h1 className="text-2xl font-bold text-accentColor">
            <Link to="/">Spectron</Link>
          </h1>
          <p className="text-gray-700 text-sm leading-relaxed">
            Spectron is an offline land change detection tool that analyzes
            multi-temporal satellite imagery (LISS-4/Sentinel) using NDVI and
            band differencing — no internet, no prior remote sensing knowledge
            needed.
          </p>
          <div className="flex gap-4 mt-2">
            <a
              href=""
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-accentColor text-xl"
            >
              <FaGithub />
            </a>
            <a
              href=""
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-accentColor text-xl"
            >
              <FaLinkedin />
            </a>
            <a
              href=""
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-accentColor text-xl"
            >
              <FaYoutube />
            </a>
          </div>
        </div>

        {/* Right - Quick Links */}
        <div className="md:w-2/3 flex flex-row justify-center gap-4 sm:gap-8">
          <div className="flex flex-col gap-2 text-sm text-gray-700">
            <h2 className="font-semibold mb-2 text-xl">Product</h2>
            <Link to="/features" className="hover:text-accentColor">
              Features
            </Link>
            <Link to="/overview" className="hover:text-accentColor">
              Overview
            </Link>
            <Link to="/compare" className="hover:text-accentColor">
              Comparison Tool
            </Link>
          </div>
          <div className="flex flex-col gap-2 text-sm text-gray-700">
            <h2 className="font-semibold mb-2 text-xl">Support</h2>
            <Link to="/docs" className="hover:text-accentColor">
              Documentation
            </Link>
            <Link to="/faq" className="hover:text-accentColor">
              FAQ
            </Link>
            <Link to="/contact" className="hover:text-accentColor">
              Contact
            </Link>
          </div>
          <div className="flex flex-col gap-2 text-sm text-gray-700">
            <h2 className="font-semibold mb-2 text-xl">Team</h2>
            <Link to="/team" className="hover:text-accentColor">
              About Us
            </Link>
            <Link to="/acknowledgements" className="hover:text-accentColor">
              Acknowledgements
            </Link>
            <Link to="/credits" className="hover:text-accentColor">
              Credits
            </Link>
          </div>
        </div>
      </div>

      <div className="w-full py-4 flex items-center justify-center">
        <p className="text-sm text-gray-600">
          © 2025 Spectron Team. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
