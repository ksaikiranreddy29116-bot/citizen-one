import Navbar from "../../components/common/Navbar";

import NotificationCard from "../../components/notifications/NotificationCard";
import TimelineStep from "../../components/notifications/TimelineStep";

function Notifications() {
  const responses = JSON.parse(
    localStorage.getItem("citizenResponses") || "{}"
  );

  const allResponses = Object.values(responses);

  const first = allResponses[0] || {};

  const notifications = first.notifications || [];
  const executionLogs = first.execution_logs || [];

  const timeline = executionLogs.map((log) => ({
    title: log,
    status: "Completed",
    time: "Just Now",
  }));

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-100 py-10 px-6">
        <div className="max-w-5xl mx-auto">

          <h1 className="text-4xl font-bold text-gray-800">
            Application Status
          </h1>

          <p className="text-gray-500 mt-2">
            Track your AI-powered application progress.
          </p>

          <div className="mt-8">

            <NotificationCard
              applicationId="CITIZENONE-001"
              scheme={
                first.recommendations?.recommended_schemes?.[0]
                  ?.scheme_name || "No Scheme Recommended"
              }
              estimatedTime="Completed"
            />

          </div>

          <div className="bg-white rounded-3xl shadow-xl p-8 mt-8">

            <h2 className="text-2xl font-bold mb-6">
              Notifications
            </h2>

            <div className="space-y-4 mb-10">

              {notifications.length > 0 ? (
                notifications.map((notification, index) => (
                  <div
                    key={index}
                    className="border rounded-xl p-4 bg-blue-50"
                  >
                    <h3 className="font-semibold text-blue-800">
                      {notification.type}
                    </h3>

                    <p className="text-gray-700 mt-1">
                      {notification.message}
                    </p>
                  </div>
                ))
              ) : (
                <p>No notifications available.</p>
              )}

            </div>

            <h2 className="text-2xl font-bold mb-6">
              AI Execution Timeline
            </h2>

            {timeline.map((step, index) => (
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