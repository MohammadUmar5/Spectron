import { useState } from "react";
import { FaCalendarPlus } from "react-icons/fa6";
import { IoMdCloseCircle } from "react-icons/io";
type WidgetProps = {
  startDate: string;
  endDate: string;
  setStartDate: (date: string) => void;
  setEndDate: (date: string) => void;
  onSubmit: () => void;
  setMode: (mode: string) => void;
  mode: string;
};

const Widget = ({
  startDate,
  endDate,
  setStartDate,
  setEndDate,
  onSubmit,
  setMode,
  mode,
}: WidgetProps) => {
  const [isCollapsed, setIsCollapsed] = useState<boolean>(true);
  console.log(setMode);
  return (
    <div className="fixed bottom-4 right-4 z-20 space-y-4">
      <button
        onClick={() => setIsCollapsed((prev) => !prev)}
        className={`text-gray-600 bg-white p-4 rounded-4xl absolute bottom-4 right-4 ${
          !isCollapsed && "hidden"
        }`}
      >
        <FaCalendarPlus />
      </button>

      <div
        className={`w-80 p-6 rounded-2xl shadow-2xl backdrop-blur-md bg-white/80 z-20 space-y-4 text-sm sform transition-all duration-300 origin-bottom-right ${
          isCollapsed
            ? "scale-0 opacity-0 pointer-events-none"
            : "scale-100 opacity-100"
        }`}
      >
        <h2 className="text-xl font-semibold text-center">Select Dates</h2>
        <button
          onClick={() => setIsCollapsed((prev) => !prev)}
          className="absolute top-7 text-gray-600 rounded-4xl "
        >
          <IoMdCloseCircle size={"25"} />
        </button>
        <hr className="border-gray-300" />

        {/* Dropdown */}
        <div>
          <label className="block mb-1 text-gray-700">Mode Selector</label>
          <select
            value={mode}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
              setMode(e.target.value)
            }
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accentColor bg-white"
          >
            <option>Exact</option>
            <option>Quality</option>
            <option>Smart</option>
          </select>
        </div>

        {/* Start Date */}
        <div>
          <label className="block mb-1 text-gray-700">Start Date</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accentColor bg-white"
          />
        </div>

        {/* End Date */}
        <div>
          <label className="block mb-1 text-gray-700">End Date</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accentColor bg-white"
          />
        </div>

        <button
          onClick={onSubmit}
          className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-200 hover:text-black transition"
        >
          Submit
        </button>
      </div>
    </div>
  );
};

export default Widget;
