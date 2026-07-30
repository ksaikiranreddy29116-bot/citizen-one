function DocumentUploadCard({
  title,
  name,
  file,
  onChange,
}) {
  return (
    <div className="border-2 border-dashed border-gray-300 rounded-2xl p-6 hover:border-blue-600 transition">

      <h2 className="text-lg font-semibold mb-4">
        {title}
      </h2>

      <input
        type="file"
        name={name}
        accept=".pdf,.jpg,.jpeg,.png"
        onChange={onChange}
        className="block w-full text-sm text-gray-600
                   file:mr-4
                   file:py-2
                   file:px-4
                   file:rounded-lg
                   file:border-0
                   file:bg-blue-600
                   file:text-white
                   hover:file:bg-blue-700
                   cursor-pointer"
      />

      {file ? (
        <div className="mt-4">

          <p className="text-green-600 font-medium">
            ✓ {file.name}
          </p>

          <p className="text-gray-500 text-sm mt-1">
            Ready for verification
          </p>

        </div>
      ) : (

        <p className="text-gray-400 text-sm mt-4">
          Supported: PDF, JPG, PNG
        </p>

      )}

    </div>
  );
}

export default DocumentUploadCard;