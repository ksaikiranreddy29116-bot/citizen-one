function MissingDocs({ documents }) {
  if (!documents.length) {
    return (
      <div className="mt-4">
        <h3 className="font-semibold text-gray-800">
          Missing Documents
        </h3>

        <p className="text-green-600 text-sm mt-2">
          None 🎉
        </p>
      </div>
    );
  }

  return (
    <div className="mt-4">
      <h3 className="font-semibold text-gray-800 mb-2">
        Missing Documents
      </h3>

      <ul className="space-y-2">
        {documents.map((doc, index) => (
          <li
            key={index}
            className="text-red-600 text-sm flex items-center gap-2"
          >
            <span>✗</span>
            <span>{doc}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MissingDocs;