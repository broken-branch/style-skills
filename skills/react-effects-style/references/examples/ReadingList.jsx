/* You Might Not Need an Effect: [you-might-not-need-an-effect:4] derive data;
   [you-might-not-need-an-effect:19] store a selection ID, not a copied item.
   items contains unique { id, title } records; missing selections show none. */
import { useState } from 'react';

export function ReadingList({ items }) {
  const [selectedId, setSelectedId] = useState(null);
  const selectedItem = items.find((item) => item.id === selectedId) ?? null;

  return (
    <section>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <button
              type="button"
              aria-pressed={item.id === selectedId}
              onClick={() => setSelectedId(item.id)}
            >
              {item.title}
            </button>
          </li>
        ))}
      </ul>
      <p>Selected: {selectedItem?.title ?? 'None'}</p>
    </section>
  );
}
