import {
  HiOutlineMap,
  HiOutlineCalendar,
  HiOutlineCloudDownload,
  HiOutlineBell,
  HiOutlineChartSquareBar,
} from "react-icons/hi";

const features = [
  {
    title: "AOI Selection",
    description:
      "Draw or select an Area of Interest (AOI) directly on the map for precise change analysis.",
    icon: HiOutlineMap,
  },
  {
    title: "Time-Based Comparison",
    description:
      "Pick two different dates to compare satellite images and detect vegetation or land cover changes.",
    icon: HiOutlineCalendar,
  },
  {
    title: "Automated Image Retrieval",
    description:
      "Automatically fetch relevant LISS-4 or Sentinel imagery for selected dates — no manual hassle.",
    icon: HiOutlineCloudDownload,
  },
  {
    title: "Change Alerts",
    description:
      "Receive smart alerts based on detected NDVI shifts or spectral band differences.",
    icon: HiOutlineBell,
  },
  {
    title: "Reports & Summaries",
    description:
      "Get visual summaries, statistics, and downloadable reports for any change analysis run.",
    icon: HiOutlineChartSquareBar,
  },
  {
    title: "Fully Offline",
    description:
      "Works without internet — lightweight, efficient, and built for field or remote use.",
    icon: HiOutlineChartSquareBar,
  },
];

const FeaturesSection = () => {
  return (
    <div className="flex flex-col items-center justify-center mt-8">
      <span className="w-full sm:w-2/3 flex flex-col items-center justify-center">
        <h1 className="text-xl uppercase opacity-75 font-extrabold text-center text-textColor">
          Key Features
        </h1>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-center text-textColor">
          Change Detection. Simplified.
        </h1>
        <p className="w-full sm:w-2/3 mt-3 text-lg sm:text-xl text-center opacity-75">
          Spectron brings remote sensing to your desktop with intelligent tools
          that work without internet or technical know-how.
        </p>
      </span>

      {/* Features Grid */}
      <div className="w-11/12 max-w-6xl mx-auto mt-16 grid grid-cols-1 md:grid-cols-2 gap-10">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-3xl shadow-xl hover:shadow-textColor/40 transition-all duration-300 hover:scale-[1.03] flex flex-col items-center text-center"
            >
              <div className="bg-textColor/20 p-4 rounded-full mb-4">
                <Icon className="text-4xl text-textColor" />
              </div>
              <h3 className="text-2xl font-semibold text-textColor mb-2 tracking-wide">
                {feature.title}
              </h3>
              <p className="text-base text-textColor/90 leading-relaxed">
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default FeaturesSection;
