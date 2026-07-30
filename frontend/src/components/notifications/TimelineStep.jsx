import StatusBadge from "./StatusBadge";

function TimelineStep({ step }) {
  return (
    <div className="flex justify-between items-center border-b py-5">

      <div>

        <h3 className="font-semibold text-lg">
          {step.title}
        </h3>

        <p className="text-gray-500 text-sm">
          {step.time}
        </p>

      </div>

      <StatusBadge status={step.status} />

    </div>
  );
}

export default TimelineStep;