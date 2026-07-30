function ReasonCard({ reasons }) {
  return (
    <div className="mt-4">
      <h3 className="font-semibold text-gray-800 mb-2">
        Why Recommended
      </h3>

      <ul className="space-y-2">
        {reasons.map((reason, index) => (
          <li
            key={index}
            className="text-green-700 text-sm flex items-center gap-2"
          >
            <span>✓</span>
            <span>{reason}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReasonCard;