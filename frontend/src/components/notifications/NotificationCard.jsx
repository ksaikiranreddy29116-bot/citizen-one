function NotificationCard({
  applicationId,
  scheme,
  estimatedTime,
}) {
  return (
    <div className="bg-white rounded-3xl shadow-xl p-8">

      <h2 className="text-2xl font-bold text-[#1E3A8A]">
        Application Tracking
      </h2>

      <div className="mt-6 space-y-3">

        <p>
          <strong>Application ID:</strong> {applicationId}
        </p>

        <p>
          <strong>Scheme:</strong> {scheme}
        </p>

        <p>
          <strong>Estimated Processing:</strong> {estimatedTime}
        </p>

      </div>

    </div>
  );
}

export default NotificationCard;