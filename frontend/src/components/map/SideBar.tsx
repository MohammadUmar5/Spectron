const SideBar = () => {
  return (
    <div className="w-74 bg-gradient-to-br from-[#f9eee0] via-[#f3e2c7] to-[#e7d4b5] border-r p-4 overflow-y-auto">
      <h2 className="text-xl font-semibold mb-4">Select Dates</h2>
      <label className="block mb-2">Start Date</label>
      <input
        type="date"
        className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accentColor"
      />

      <label className="block mb-2">End Date</label>
      <input
        type="date"
        className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-accentColor"
      />

      <button className="btn bg-accentColor p-3 rounded-lg m-2 text-white hover:text-accentColor hover:bg-yellow-100 transition-all">
        Submit
      </button>
    </div>
  );
};

export default SideBar;
