import Navbar from "../../components/common/Navbar";
import AgentTimeline from "../../components/recommendations/AgentTimeline";
import RecommendationCard from "../../components/recommendations/RecommendationCard";

import timeline from "../../mock/timeline.json";

function Recommendations() {
  const responses = JSON.parse(
    localStorage.getItem("citizenResponses") || "{}"
  );

  const allResponses = Object.values(responses);

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-100 py-10 px-6">
        <div className="max-w-7xl mx-auto">

          <div className="mb-10">
            <h1 className="text-4xl font-bold text-gray-800">
              AI Recommendations
            </h1>

            <p className="text-gray-600 mt-2">
              CitizenOne AI has analyzed your uploaded documents.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            <div className="lg:col-span-1">
              <AgentTimeline timeline={timeline} />
            </div>

            <div className="lg:col-span-2 space-y-6">

              {allResponses.map((response, index) => {

                const schemes =
                  response.recommendations
                    ?.recommended_schemes || [];

                if (schemes.length === 0) {
                  return (
                    <div
                      key={index}
                      className="bg-white rounded-2xl shadow-lg p-6"
                    >
                      <h2 className="text-xl font-bold text-red-600">
                        No Eligible Schemes
                      </h2>

                      <p className="mt-3 text-gray-600">
                        {response.explanation}
                      </p>
                    </div>
                  );
                }

                return schemes.map((scheme) => (
                  <RecommendationCard
                    key={scheme.scheme_id}
                    scheme={scheme}
                    matchingCriteria={
                      response.matching_criteria
                    }
                    documentsUtilized={
                      response.documents_utilized
                    }
                    missingRequirements={
                      response.missing_requirements
                    }
                  />
                ));
              })}

            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6 mt-10">

            <h2 className="text-2xl font-bold mb-5">
              Next Steps
            </h2>

            <ul className="list-disc pl-5 space-y-3">
              {allResponses.flatMap((response) =>
                response.recommendations.next_steps.map(
                  (step, index) => (
                    <li key={index}>{step}</li>
                  )
                )
              )}
            </ul>

          </div>

        </div>
      </section>
    </>
  );
}

export default Recommendations;