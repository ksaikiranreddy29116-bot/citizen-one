import Navbar from "../../components/common/Navbar";
import { Link } from "react-router-dom";

import ApplicationSection from "../../components/application/ApplicationSection";
import FieldRow from "../../components/application/FieldRow";
import AttachedDocument from "../../components/application/AttachedDocument";
import AINotes from "../../components/application/AINotes";

function ApplicationReview() {
  const responses = JSON.parse(
    localStorage.getItem("citizenResponses") || "{}"
  );

  const allResponses = Object.values(responses);

  const first = allResponses[0] || {};

  const extracted = first.extracted_data || {};
  const eligibility = first.eligibility || {};

  const documents = allResponses.map((response) => ({
    name: response.extracted_data.document_type,
    status: "Verified",
  }));

  const notes = [
    first.explanation,
    ...(eligibility.rule_validations || []).map(
      (rule) =>
        `${rule.rule_name}: ${
          rule.passed ? "PASSED" : "FAILED"
        } - ${rule.reason}`
    ),
  ];

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-100 py-10 px-6">
        <div className="max-w-6xl mx-auto">

          <div className="bg-white rounded-3xl shadow-xl p-8 mb-8">

            <h1 className="text-4xl font-bold">
              Citizen Application Review
            </h1>

            <p className="text-gray-500 mt-2">
              Generated automatically by CitizenOne AI
            </p>

            <div
              className={`mt-5 inline-block px-5 py-2 rounded-full font-semibold ${
                eligibility.eligible
                  ? "bg-green-100 text-green-700"
                  : "bg-red-100 text-red-700"
              }`}
            >
              {eligibility.eligible
                ? "Eligible"
                : "Not Eligible"}
            </div>

          </div>

          <div className="grid lg:grid-cols-2 gap-8">

            <ApplicationSection title="Personal Details">

              <FieldRow
                label="Name"
                value={extracted.full_name || "-"}
              />

              <FieldRow
                label="Date of Birth"
                value={extracted.dob || "-"}
              />

              <FieldRow
                label="Gender"
                value={extracted.gender || "-"}
              />

            </ApplicationSection>

            <ApplicationSection title="Address">

              <FieldRow
                label="State"
                value={extracted.state || "-"}
              />

              <FieldRow
                label="District"
                value={extracted.district || "-"}
              />

            </ApplicationSection>

            <ApplicationSection title="Income Details">

              <FieldRow
                label="Annual Income"
                value={
                  extracted.income_annual ?? "Not Available"
                }
              />

              <FieldRow
                label="Aadhaar Number"
                value={
                  extracted.aadhaar_number ??
                  "Not Available"
                }
              />

            </ApplicationSection>

            <ApplicationSection title="Uploaded Documents">

              {documents.map((doc) => (
                <AttachedDocument
                  key={doc.name}
                  document={doc}
                />
              ))}

            </ApplicationSection>

          </div>

          <div className="mt-8">

            <AINotes notes={notes} />

          </div>

          <div className="flex justify-end gap-5 mt-10">

            <button className="border border-[#1E3A8A] text-[#1E3A8A] px-6 py-3 rounded-xl hover:bg-blue-50 transition">
              Edit
            </button>

            <Link
              to="/notifications"
              className="bg-[#1E3A8A] hover:bg-blue-800 text-white px-6 py-3 rounded-xl transition"
            >
              Submit Application
            </Link>

          </div>

        </div>
      </section>
    </>
  );
}

export default ApplicationReview;