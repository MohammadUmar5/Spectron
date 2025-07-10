import { FeaturesSection, HeroSection } from "../../components";
import { LandingWrapper } from "../../hoc";

const Landing = () => {
  return (
    <>
      <HeroSection />
      <FeaturesSection />
    </>
  );
};

export default LandingWrapper(Landing);
