function Hero() {
  return (
    <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-24">
      <div className="max-w-7xl mx-auto px-8">

        <h1 className="text-6xl font-bold leading-tight">
          Government Schemes
          <br />
          Should Find You
        </h1>

        <p className="mt-6 text-xl max-w-2xl text-blue-100">
          CitizenOne uses AI to discover welfare schemes,
          verify your documents and simplify applications.
        </p>

        <button
          className="mt-10 bg-white text-blue-700 font-semibold px-8 py-4 rounded-lg hover:bg-gray-100 transition"
        >
          Get Started
        </button>

      </div>
    </section>
  );
}

export default Hero;