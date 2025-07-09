import { Route, Routes } from "react-router-dom";
import { About, Home } from "./pages";

function App() {
  return (
    <div className="w-screen min-h-screen">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  );
}

export default App;
