function ApplicationSection({ title, children }) {
  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">

      <h2 className="text-xl font-bold mb-5">
        {title}
      </h2>

      {children}

    </div>
  );
}

export default ApplicationSection;