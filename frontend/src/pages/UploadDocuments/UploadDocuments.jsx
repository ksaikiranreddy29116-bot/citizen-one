import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/common/Navbar";
import DocumentUploadCard from "../../components/upload/DocumentUploadCard";
import { documentTypes } from "../../constants/documentTypes";
import { extractDocument } from "../../api/ai";

function UploadDocuments() {
  const [documents, setDocuments] = useState({
    aadhaar: null,
    income: null,
    caste: null,
    domicile: null,
  });
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setDocuments({
      ...documents,
      [e.target.name]: e.target.files[0],
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const uploadedResponses = {};

    for (const [key, file] of Object.entries(documents)) {
      if (!file) continue;

      console.log(`Uploading ${key}...`);

      const response = await extractDocument(file);

      uploadedResponses[key] = response;
    }

    console.log("All Responses:", uploadedResponses);

    localStorage.setItem(
      "citizenResponses",
      JSON.stringify(uploadedResponses)
    );

    navigate("/processing");
  } catch (error) {
  console.error("FULL ERROR:", error);

  if (error.response) {
    console.log("Status:", error.response.status);
    console.log("Response:", error.response.data);
  } else if (error.request) {
    console.log("Request:", error.request);
  } else {
    console.log("Message:", error.message);
  }

  alert(error.message);
}
};

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-slate-50 px-6 py-10">

        <div className="max-w-6xl mx-auto">

          <h1 className="text-4xl font-bold text-gray-800">
            Upload Documents
          </h1>

          <p className="text-gray-500 mt-2">
            Upload your documents securely for AI verification.
          </p>

          <form
            onSubmit={handleSubmit}
            className="mt-10 bg-white shadow-xl rounded-3xl p-8"
          >

            <div className="grid md:grid-cols-2 gap-8">

              {documentTypes.map((doc) => (
                <DocumentUploadCard
                  key={doc.name}
                  title={doc.title}
                  name={doc.name}
                  file={documents[doc.name]}
                  onChange={handleFileChange}
                />
              ))}

            </div>

            <button
              type="submit"
              className="mt-10 w-full bg-[#1E3A8A] hover:bg-blue-800 text-white py-4 rounded-xl text-lg font-semibold transition"
            >
              Upload & Verify Documents
            </button>

          </form>

        </div>

      </section>
    </>
  );
}

export default UploadDocuments;