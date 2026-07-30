import Navbar from "../../components/common/Navbar";
import { Link } from "react-router-dom";
function Dashboard() {
  const stats = [
    {
      title: "Eligible Schemes",
      value: 8,
      color: "bg-blue-100 text-blue-700",
    },
    {
      title: "Applications",
      value: 3,
      color: "bg-green-100 text-green-700",
    },
    {
      title: "Documents",
      value: 5,
      color: "bg-yellow-100 text-yellow-700",
    },
    {
      title: "Notifications",
      value: 2,
      color: "bg-red-100 text-red-700",
    },
  ];

  const schemes = [
    "PM Kisan",
    "National Scholarship",
    "Ayushman Bharat",
  ];

  const applications = [
    {
      scheme: "PM Kisan",
      status: "Approved",
      date: "20 Jul 2026",
    },
    {
      scheme: "Scholarship",
      status: "Under Review",
      date: "15 Jul 2026",
    },
    {
      scheme: "Housing Scheme",
      status: "Submitted",
      date: "12 Jul 2026",
    },
  ];

  const notifications = [
    "New Scholarship Scheme Available",
    "Income Certificate expires in 10 days",
    "PM Kisan application approved",
  ];

  return (
    <>
      <Navbar />

      <section className="bg-slate-50 min-h-screen px-8 py-8">

        {/* Welcome */}

        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800">
            Welcome Back 👋
          </h1>
          <div className="flex gap-4 mt-6">

  <Link
    to="/upload-documents"
    className="bg-[#1E3A8A] hover:bg-blue-800 text-white px-6 py-3 rounded-xl font-semibold transition"
  >
    Upload Documents
  </Link>

</div>
          <p className="text-gray-600 mt-2">
            Here's what's happening with your CitizenOne profile.
          </p>
        </div>

        {/* Stats */}

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">

          {stats.map((item) => (
            <div
              key={item.title}
              className="bg-white rounded-2xl shadow-md p-6"
            >
              <h3 className="text-gray-500">
                {item.title}
              </h3>

              <h1 className={`text-4xl font-bold mt-3 ${item.color}`}>
                {item.value}
              </h1>
            </div>
          ))}

        </div>

        {/* Main Grid */}

        <div className="grid lg:grid-cols-3 gap-8">

          {/* Left */}

          <div className="lg:col-span-2 space-y-8">

            {/* AI Recommendations */}

            <div className="bg-white rounded-2xl shadow-md p-6">

              <h2 className="text-2xl font-semibold mb-5">
                AI Recommended Schemes
              </h2>

              <div className="grid md:grid-cols-3 gap-5">

                {schemes.map((scheme) => (
                  <div
                    key={scheme}
                    className="border rounded-xl p-5 hover:shadow-lg transition"
                  >
                    <h3 className="font-semibold text-lg">
                      {scheme}
                    </h3>

                    <p className="text-gray-500 mt-2">
                      You are likely eligible.
                    </p>

                    <button className="mt-5 bg-[#1E3A8A] text-white px-4 py-2 rounded-lg">
                      View
                    </button>
                  </div>
                ))}

              </div>

            </div>

            {/* Applications */}

            <div className="bg-white rounded-2xl shadow-md p-6">

              <h2 className="text-2xl font-semibold mb-5">
                Recent Applications
              </h2>

              <table className="w-full">

                <thead>

                  <tr className="text-left border-b">

                    <th className="py-3">Scheme</th>

                    <th>Status</th>

                    <th>Date</th>

                  </tr>

                </thead>

                <tbody>

                  {applications.map((app) => (
                    <tr
                      key={app.scheme}
                      className="border-b"
                    >
                      <td className="py-4">
                        {app.scheme}
                      </td>

                      <td>{app.status}</td>

                      <td>{app.date}</td>

                    </tr>
                  ))}

                </tbody>

              </table>

            </div>

          </div>

          {/* Right */}

          <div className="space-y-8">

            {/* Notifications */}

            <div className="bg-white rounded-2xl shadow-md p-6">

              <h2 className="text-2xl font-semibold mb-5">
                Notifications
              </h2>

              <ul className="space-y-4">

                {notifications.map((item) => (
                  <li
                    key={item}
                    className="border-b pb-3"
                  >
                    {item}
                  </li>
                ))}

              </ul>

            </div>

            {/* Profile */}

            <div className="bg-white rounded-2xl shadow-md p-6">

              <h2 className="text-2xl font-semibold mb-5">
                Profile Completion
              </h2>

              <div className="w-full bg-gray-200 rounded-full h-4">

                <div
                  className="bg-green-500 h-4 rounded-full"
                  style={{ width: "80%" }}
                />

              </div>

              <p className="mt-3 text-gray-600">
                80% Complete
              </p>
                <Link to="/upload-documents">
  Upload Documents
</Link>
              

            </div>

          </div>

        </div>

      </section>
    </>
  );
}

export default Dashboard;