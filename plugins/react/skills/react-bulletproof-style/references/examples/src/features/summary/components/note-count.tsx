/* Bulletproof React: [bulletproof-react:5] no cross-feature imports;
   [bulletproof-react:30] focused props; [bulletproof-react:31] defer sharing.
   This feature accepts a count without depending on the notes feature. */
export function NoteCount({ count }: { count: number }) {
  return <p>{count} notes in the collection.</p>;
}
