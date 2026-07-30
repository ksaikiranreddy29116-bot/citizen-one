function Features() {
  return (
    <section className="py-20">

      <h2 className="text-4xl font-bold text-center">
        Features
      </h2>

      <div className="grid grid-cols-3 gap-8 max-w-6xl mx-auto mt-12">

        <div className="shadow-lg p-8 rounded-xl">
          <h3 className="text-2xl font-semibold">
            AI Recommendations
          </h3>

          <p className="mt-4">
            Discover schemes matching your profile instantly.
          </p>
        </div>

        <div className="shadow-lg p-8 rounded-xl">
          <h3 className="text-2xl font-semibold">
            Document Verification
          </h3>

          <p className="mt-4">
            Upload certificates and verify them using AI.
          </p>
        </div>

        <div className="shadow-lg p-8 rounded-xl">
          <h3 className="text-2xl font-semibold">
            Smart Reminders
          </h3>

          <p className="mt-4">
            Never miss an application deadline again.
          </p>
        </div>

      </div>

    </section>
  );
}

export default Features;