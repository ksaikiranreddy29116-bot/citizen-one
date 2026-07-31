import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

function AIProcessing() {
  const navigate = useNavigate();

  const [completed, setCompleted] = useState([]);

  const steps = useMemo(() => {
    const responses = JSON.parse(
      localStorage.getItem("citizenResponses") || "{}"
    );

    const uploadedDocs = Object.keys(responses);

    return [
      ...uploadedDocs.map(
        (doc) => `Processing ${doc.toUpperCase()} Document...`
      ),
      "Verifying Eligibility...",
      "Finding Welfare Schemes...",
      "Generating AI Explanation...",
      "Preparing Recommendations...",
    ];
  }, []);

  useEffect(() => {
    let index = 0;

    const interval = setInterval(() => {
      if (index < steps.length) {
        setCompleted((prev) => [...prev, steps[index]]);
        index++;
      } else {
        clearInterval(interval);

        setTimeout(() => {
          navigate("/recommendations");
        }, 1500);
      }
    }, 800);

    return () => clearInterval(interval);
  }, [navigate, steps]);

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-6">
      <div className="bg-slate-800 rounded-2xl shadow-2xl p-10 w-full max-w-4xl">
        <div className="flex items-center gap-4 mb-8">
          <div className="w-14 h-14 rounded-full bg-blue-600 flex items-center justify-center text-white text-2xl">
            🤖
          </div>

          <div>
            <h1 className="text-3xl font-bold text-white">
              CitizenOne AI Agent
            </h1>

            <p className="text-slate-300">
              Processing Uploaded Documents...
            </p>
          </div>
        </div>

        <div className="space-y-5">
          {steps.map((step, index) => {
            const done = completed.includes(step);

            return (
              <div
                key={index}
                className="flex items-center justify-between border-b border-slate-700 pb-4"
              >
                <span className="text-slate-200">{step}</span>

                {done ? (
                  <span className="text-green-400 font-semibold">
                    ✔ Completed
                  </span>
                ) : (
                  <span className="text-yellow-400 animate-pulse">
                    Processing...
                  </span>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-10">
          <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="bg-green-500 h-full transition-all duration-700"
              style={{
                width: `${
                  steps.length
                    ? (completed.length / steps.length) * 100
                    : 0
                }%`,
              }}
            />
          </div>

          <p className="text-slate-400 mt-4 text-center">
            {completed.length === steps.length
              ? "AI analysis completed. Redirecting..."
              : "CitizenOne AI is analyzing your documents..."}
          </p>
        </div>
      </div>
    </div>
  );
}

export default AIProcessing;