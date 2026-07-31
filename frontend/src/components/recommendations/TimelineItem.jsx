function TimelineItem({ agent, message, time, status }) {
  return (
    <div className="flex items-start gap-3 pb-5">

      <div
        className={`mt-1 h-3 w-3 rounded-full ${
          status === "completed"
            ? "bg-green-500"
            : "bg-yellow-500"
        }`}
      />

      <div>

        <h4 className="font-semibold text-gray-800">
          {agent}
        </h4>

        <p className="text-sm text-gray-600">
          {message}
        </p>

        <span className="text-xs text-gray-400">
          {time}
        </span>

      </div>

    </div>
  );
}

export default TimelineItem;