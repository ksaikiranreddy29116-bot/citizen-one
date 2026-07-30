import Navbar from "../../components/common/Navbar";

import NotificationCard from "../../components/notifications/NotificationCard.jsx";
import TimelineStep from "../../components/notifications/TimelineStep";

import data from "../../mock/notifications.json";

function Notifications() {
  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-100 py-10 px-6">

        <div className="max-w-5xl mx-auto">

          <h1 className="text-4xl font-bold text-gray-800">
            Application Status
          </h1>

          <p className="text-gray-500 mt-2">
            Track your application and receive AI-powered updates.
          </p>

          <div className="mt-8">

            <NotificationCard
              applicationId={data.applicationId}
              scheme={data.scheme}
              estimatedTime={data.estimatedTime}
            />

          </div>

          <div className="bg-white rounded-3xl shadow-xl p-8 mt-8">

            <h2 className="text-2xl font-bold mb-6">
              Status Timeline
            </h2>

            {data.timeline.map((step, index) => (

              <TimelineStep
                key={index}
                step={step}
              />

            ))}

          </div>

        </div>

      </section>
    </>
  );
}

export default Notifications;