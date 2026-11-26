/* Bulletproof React: [bulletproof-react:4] direct imports, no barrel;
   [bulletproof-react:5] app composes features; [bulletproof-react:6] imports
   point from app to features. Short relative paths need no alias setup. */
import { NoteList } from '../features/notes/components/note-list';
import type { Note } from '../features/notes/components/note-list';
import { NoteCount } from '../features/summary/components/note-count';

export function NotesPage({ notes }: { notes: readonly Note[] }) {
  return (
    <main>
      <h1>Notes</h1>
      <NoteCount count={notes.length} />
      <NoteList notes={notes} />
    </main>
  );
}
