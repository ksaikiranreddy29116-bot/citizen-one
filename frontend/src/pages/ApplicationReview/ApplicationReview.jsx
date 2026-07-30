import Navbar from "../../components/common/Navbar";

import ApplicationSection from "../../components/application/ApplicationSection";
import FieldRow from "../../components/application/FieldRow";
import AttachedDocument from "../../components/application/AttachedDocument";
import AINotes from "../../components/application/AINotes";

import application from "../../mock/application.json";
import { Link } from "react-router-dom";

function ApplicationReview() {
  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-100 py-10 px-6">

        <div className="max-w-6xl mx-auto">

          <div className="bg-white rounded-3xl shadow-xl p-8 mb-8">

            <h1 className="text-4xl font-bold">
              {application.scheme}
            </h1>

            <p className="text-gray-500 mt-2">
              Application generated automatically by CitizenOne AI
            </p>

            <div className="mt-5 inline-block bg-green-100 text-green-700 px-5 py-2 rounded-full font-semibold">
              {application.confidence}% Confidence
            </div>

          </div>

          <div className="grid lg:grid-cols-2 gap-8">

            <ApplicationSection title="Personal Details">

              <FieldRow
                label="Name"
                value={application.personal.name}
              />

              <FieldRow
                label="Date of Birth"
                value={application.personal.dob}
              />

              <FieldRow
                label="Gender"
                value={application.personal.gender}
              />

            </ApplicationSection>

            <ApplicationSection title="Address">

              <FieldRow
                label="State"
                value={application.address.state}
              />

              <FieldRow
                label="District"
                value={application.address.district}
              />

              <FieldRow
                label="Pincode"
                value={application.address.pincode}
              />

            </ApplicationSection>

            <ApplicationSection title="Income Details">

              <FieldRow
                label="Annual Income"
                value={application.income.annualIncome}
              />

              <FieldRow
                label="Occupation"
                value={application.income.occupation}
              />

            </ApplicationSection>

            <ApplicationSection title="Attached Documents">

              {application.documents.map((doc) => (

                <AttachedDocument
                  key={doc.name}
                  document={doc}
                />

              ))}

            </ApplicationSection>

          </div>

          <div className="mt-8">

            <AINotes
              notes={application.notes}
            />

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