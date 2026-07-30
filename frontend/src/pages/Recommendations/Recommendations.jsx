import Navbar from "../../components/common/Navbar";
import AgentTimeline from "../../components/recommendations/AgentTimeline";
import RecommendationCard from "../../components/recommendations/RecommendationCard";

import timeline from "../../mock/timeline.json";
import recommendations from "../../mock/recommendations.json";

function Recommendations() {
  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-100 py-10 px-6">

        <div className="max-w-7xl mx-auto">

          {/* Header */}

          <div className="mb-10">

            <h1 className="text-4xl font-bold text-gray-800">
              AI Recommendations
            </h1>

            <p className="text-gray-600 mt-2">
              CitizenOne AI has analyzed your profile, verified your
              uploaded documents and prepared personalized scheme
              recommendations.
            </p>

          </div>

          {/* Two Column Layout */}

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Left */}

            <div className="lg:col-span-1">

              <AgentTimeline timeline={timeline} />

            </div>

            {/* Right */}

            <div className="lg:col-span-2 space-y-6">

              {recommendations.map((recommendation) => (

                <RecommendationCard
                  key={recommendation.scheme_id}
                  recommendation={recommendation}
                />

              ))}

            </div>

          </div>

          {/* Next Steps */}

          <div className="bg-white rounded-2xl shadow-lg p-6 mt-10">

            <h2 className="text-2xl font-bold mb-5">
              📋 Next Steps
            </h2>

            <ol className="space-y-4 list-decimal list-inside">

              <li className="text-gray-700">
                Review the AI generated application draft.
              </li>

              <li className="text-gray-700">
                Upload any missing supporting documents.
              </li>

              <li className="text-gray-700">
                Submit the application through CitizenOne.
              </li>

            </ol>

          </div>

        </div>

      </section>

    </>
  );
}

export default Recommendations;