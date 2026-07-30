function FieldRow({ label, value }) {
  return (
    <div className="flex justify-between border-b py-3">
      <span className="font-medium text-gray-600">
        {label}
      </span>

      <span className="text-gray-900">
        {value}
      </span>
    </div>
  );
}

export default FieldRow;