import { Route, Routes } from "react-router-dom";
import {
  About,
  Dashboard,
  Docs,
  Features,
  Login,
  NotFound,
  Signup,
} from "./pages";
import { ProtectedRoute, RedirectToDashboard } from "./components";

function App() {
  return (
    <Routes>
      {/* Public Paths */}
      <Route index path="/" element={<RedirectToDashboard />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/about" element={<About />} />
      <Route path="/features" element={<Features />} />
      <Route path="/docs" element={<Docs />} />

      {/* Protected Paths */}
      <Route
        path="/dashboard"
        element={<ProtectedRoute element={<Dashboard />} />}
      />

      {/* Catch-all route for undefined paths */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
