import MatchBadge from "./MatchBadge";
import ReasonCard from "./ReasonCard";
import MissingDocs from "./MissingDocs";
import { Link } from "react-router-dom";

function RecommendationCard({
  scheme,
  matchingCriteria,
  documentsUtilized,
  missingRequirements,
}) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">
            {scheme.scheme_name}
          </h2>

          <p className="text-gray-500">
            Scheme ID: {scheme.scheme_id}
          </p>
        </div>

        <MatchBadge
          match={Math.round(scheme.match_score * 100)}
        />
      </div>

      <ReasonCard reasons={scheme.reasoning} />

      <div className="mt-5">
        <h3 className="font-semibold text-gray-800 mb-2">
          Matching Criteria
        </h3>

        <div className="flex flex-wrap gap-2">
          {matchingCriteria.map((item) => (
            <span
              key={item}
              className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
            >
              {item}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-5">
        <h3 className="font-semibold text-gray-800 mb-2">
          Documents Used
        </h3>

        <div className="flex flex-wrap gap-2">
          {documentsUtilized.map((doc) => (
            <span
              key={doc}
              className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
            >
              {doc}
            </span>
          ))}
        </div>
      </div>

      <MissingDocs documents={missingRequirements} />

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