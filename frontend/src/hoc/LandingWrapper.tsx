import React from "react";
import { Footer, NavBar } from "../components";

const LandingWrapper = <P extends object>(
  WrappedComponent: React.ComponentType<P>
) => {
  const ComponentWithWrapper = (props: P) => {
    return (
      <section className="w-screen min-h-screen flex flex-col items-center bg-gradient-to-br from-[#f9eee0] via-[#f3e2c7] to-[#e7d4b5]">
        <div className="w-full min-h-screen overflow-x-hidden px-12 py-8">
          <NavBar />
          <WrappedComponent {...props} />
        </div>
        <Footer />
      </section>
    );
  };

  return ComponentWithWrapper;
};

export default LandingWrapper;
