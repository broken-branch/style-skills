/* You Might Not Need an Effect: [you-might-not-need-an-effect:12] key reset;
   [you-might-not-need-an-effect:13] wrapper owns the reset contract;
   [you-might-not-need-an-effect:3] interaction work stays in its handler.
   A new document ID resets the draft; same-ID edits preserve unsaved text. */
import { useId, useState } from 'react';

function DraftForm({ initialText, onSave }) {
  const inputId = useId();
  const [text, setText] = useState(initialText);

  return (
    <form onSubmit={(event) => {
      event.preventDefault();
      onSave(text);
    }}>
      <label htmlFor={inputId}>Draft</label>
      <textarea
        id={inputId}
        value={text}
        onChange={(event) => setText(event.target.value)}
      />
      <button type="submit">Save draft</button>
    </form>
  );
}

export function DraftEditor({ document, onSave }) {
  return (
    <DraftForm
      key={document.id}
      initialText={document.text}
      onSave={onSave}
    />
  );
}
