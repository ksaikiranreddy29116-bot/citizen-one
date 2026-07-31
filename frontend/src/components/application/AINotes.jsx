function AINotes({ notes }) {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-2xl p-6">

      <h2 className="text-xl font-bold text-blue-900 mb-4">
        🤖 CitizenOne AI Notes
      </h2>

      <ul className="space-y-3">

        {notes.map((note, index) => (

          <li
            key={index}
            className="text-blue-800"
          >
            ✓ {note}
          </li>

        ))}

      </ul>

    </div>
  );
}

export default AINotes;