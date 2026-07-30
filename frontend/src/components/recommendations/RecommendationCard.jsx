import MatchBadge from "./MatchBadge";
import ReasonCard from "./ReasonCard";
import MissingDocs from "./MissingDocs";
import { Link } from "react-router-dom";

function RecommendationCard({ recommendation }) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">

      <div className="flex justify-between items-center">

        <div>
          <h2 className="text-2xl font-bold">
            {recommendation.scheme_name}
          </h2>

          <p className="text-gray-500">
            {recommendation.category}
          </p>
        </div>

        <MatchBadge
          match={Math.round(recommendation.match_score * 100)}
        />

      </div>

      <ReasonCard
        reasons={recommendation.matching_criteria}
      />

      <div className="mt-5">

        <h3 className="font-semibold text-gray-800 mb-2">
          Documents Used
        </h3>

        <div className="flex flex-wrap gap-2">

          {recommendation.documents_utilized.map((doc) => (
            <span
              key={doc}
              className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
            >
              {doc}
            </span>
          ))}

        </div>

      </div>

      <MissingDocs
        documents={recommendation.missing_requirements}
      />

      <div className="mt-6 flex gap-4">

  <Link
    to="/application-review"
    className="bg-[#1E3A8A] text-white px-5 py-2 rounded-lg hover:bg-blue-800 transition text-center"
  >
    View Draft
  </Link>

  <button className="border border-[#1E3A8A] text-[#1E3A8A] px-5 py-2 rounded-lg hover:bg-blue-50 transition">
    Review
  </button>

</div>

    </div>
  );
}

export default RecommendationCard;