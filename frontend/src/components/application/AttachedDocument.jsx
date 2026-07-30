function AttachedDocument({ document }) {
  return (
    <div className="flex justify-between py-3 border-b">

      <span>
        {document.name}
      </span>

      {document.status === "Attached" ? (

        <span className="text-green-600 font-semibold">
          ✓ Attached
        </span>

      ) : (

        <span className="text-red-600 font-semibold">
          ✗ Missing
        </span>

      )}

    </div>
  );
}

export default AttachedDocument;