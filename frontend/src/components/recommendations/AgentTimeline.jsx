import TimelineItem from "./TimelineItem";

function AgentTimeline({ timeline }) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">

      <h2 className="text-xl font-bold mb-6">
        🤖 AI Activity Timeline
      </h2>

      {timeline.map((step, index) => (
        <TimelineItem
          key={index}
          agent={step.agent}
          message={step.message}
          time={step.time}
          status={step.status}
        />
      ))}

    </div>
  );
}

export default AgentTimeline;