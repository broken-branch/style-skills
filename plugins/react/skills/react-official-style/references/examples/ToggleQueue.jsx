/* Rules of React: [rules-of-react:27] Hooks before conditional returns;
   [rules-of-react:15] replace state; [rules-of-react:6] event-driven changes.
   initialEntries is an immutable starting snapshot of { id, title, done }. */
import { useState } from 'react';

export function ToggleQueue({ initialEntries, hidden = false }) {
  const [entries, setEntries] = useState(initialEntries);

  if (hidden) {
    return null;
  }

  function toggleEntry(id) {
    setEntries((current) => current.map((entry) => (
      entry.id === id ? { ...entry, done: !entry.done } : entry
    )));
  }

  return (
    <ul>
      {entries.map((entry) => (
        <li key={entry.id}>
          <button
            type="button"
            aria-pressed={entry.done}
            onClick={() => toggleEntry(entry.id)}
          >
            {entry.title}
          </button>
        </li>
      ))}
    </ul>
  );
}
