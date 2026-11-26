/* Bulletproof React: [bulletproof-react:1] feature ownership;
   [bulletproof-react:26] kebab-case; [bulletproof-react:43] local state.
   Kept in the feature until another consumer needs to own the filter. */
import { useId, useState } from 'react';

export interface Note {
  id: string;
  title: string;
}

export function NoteList({ notes }: { notes: readonly Note[] }) {
  const filterId = useId();
  const [filter, setFilter] = useState('');
  const visibleNotes = notes.filter((note) =>
    note.title.toLowerCase().includes(filter.toLowerCase()),
  );

  return (
    <section>
      <label htmlFor={filterId}>Filter notes</label>
      <input
        id={filterId}
        value={filter}
        onChange={(event) => setFilter(event.target.value)}
      />
      <ul>
        {visibleNotes.map((note) => <li key={note.id}>{note.title}</li>)}
      </ul>
    </section>
  );
}
