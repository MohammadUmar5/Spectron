import { useState } from "react";
import {
  FaUser,
  FaMapMarkedAlt,
  FaCalendarAlt,
  FaChartBar,
  FaTools,
  FaCog,
  FaQuestionCircle,
  FaSignOutAlt,
  FaBars,
  FaArrowCircleLeft,
} from "react-icons/fa";

type SidebarItem = {
  name: string;
  icon: JSX.Element;
};

const sidebarItems: SidebarItem[] = [
  { name: "Profile", icon: <FaUser /> },
  { name: "Map View", icon: <FaMapMarkedAlt /> },
  { name: "Change Detection", icon: <FaCalendarAlt /> },
  { name: "Insights", icon: <FaChartBar /> },
  { name: "Tools", icon: <FaTools /> },
  { name: "Settings", icon: <FaCog /> },
  { name: "Help", icon: <FaQuestionCircle /> },
  { name: "Logout", icon: <FaSignOutAlt /> },
];

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div
      className={`h-screen   bg-white shadow-xl p-4 flex flex-col items-center transition-all duration-300 ${
        isCollapsed ? "w-16" : "w-64"
      }`}
    >
      {/* Toggle Button */}
      <button
        onClick={() => setIsCollapsed((prev) => !prev)}
        className={`mb-6  text-gray-600 hover:text-gray-900 ${
          isCollapsed ? "" : "self-end"
        }`}
      >
        {isCollapsed ? <FaBars /> : <FaArrowCircleLeft size={"20"} />}
      </button>

      {/* Sidebar Items */}
      <nav className="flex flex-col gap-4">
        {sidebarItems.map((item) => (
          <div
            key={item.name}
            className="flex items-center cursor-pointer p-2 rounded-lg hover:bg-blue-50 text-gray-700 transition-colors"
          >
            <div className="text-lg">{item.icon}</div>
            {!isCollapsed && <span className="ml-4">{item.name}</span>}
          </div>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
