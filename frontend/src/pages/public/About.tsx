import { LandingWrapper } from "../../hoc";

const AboutSections = [
  {
    title: "Detect Changes Visually",
    content:
      "Spectron simplifies complex satellite analysis into a visual experience. Draw your Area of Interest, select two dates, and instantly generate intuitive change maps — no scripting, coding, or technical expertise needed.",
  },
  {
    title: "Smart Detection, Zero Guesswork",
    content:
      "With NDVI and spectral band differencing under the hood, Spectron pinpoints real vegetation and land cover changes — cutting through noise, minimizing false alarms, and ensuring what you see is meaningful.",
  },
  {
    title: "Works Anywhere, Even Offline",
    content:
      "Built to function without internet, Spectron is your go-to field tool. Lightweight yet powerful, it works in labs, classrooms, or remote areas where connectivity is limited but insights are critical.",
  },
  {
    title: "Built for Everyone",
    content:
      "Whether you're a researcher, student, policymaker, or conservationist — Spectron makes Earth observation accessible to all. No remote sensing background required, just curiosity and a purpose.",
  },
];

const About = () => {
  return (
    <>
      {AboutSections.map((section, index) => (
        <section
          key={index}
          className="max-w-7xl mx-auto px-4 py-12 text-center bg-white/20 backdrop-blur-lg rounded-2xl shadow-xl mt-8 flex items-center justify-center"
        >
          <div className="max-w-3xl">
            <h1 className="text-6xl mb-6 px-8 text-textColor font-extrabold">
              {section.title}
            </h1>
            <p className="text-xl px-8 font-semibold mb-4 text-textColor/80 opacity-85">
              {section.content}
            </p>
          </div>
        </section>
      ))}
    </>
  );
};

export default LandingWrapper(About);
