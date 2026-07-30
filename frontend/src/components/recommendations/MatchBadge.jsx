function MatchBadge({ match }) {
  let bg = "bg-red-100 text-red-700";

  if (match >= 90)
    bg = "bg-green-100 text-green-700";
  else if (match >= 75)
    bg = "bg-yellow-100 text-yellow-700";

  return (
    <span
      className={`px-4 py-2 rounded-full text-sm font-semibold ${bg}`}
    >
      {match}% Match
    </span>
  );
}

export default MatchBadge;