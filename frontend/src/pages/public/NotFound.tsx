import { LandingWrapper } from "../../hoc";

const NotFound = () => {
  return (
    <div className="text-center mt-20">
      <h1 className="text-4xl font-bold">404 - Page Not Found</h1>
      <p className="mt-4">Oops! The page you are looking for doesn't exist.</p>
    </div>
  );
};

export default LandingWrapper(NotFound);
