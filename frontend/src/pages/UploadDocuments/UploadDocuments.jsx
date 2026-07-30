import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/common/Navbar";
import DocumentUploadCard from "../../components/upload/DocumentUploadCard";
import { documentTypes } from "../../constants/documentTypes";

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

  const handleSubmit = (e) => {
  e.preventDefault();

  console.log("Uploaded Documents:", documents);

  navigate("/processing");
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