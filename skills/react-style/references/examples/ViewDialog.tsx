/* [REACT-EFFECTS] interaction work stays in handlers; [REACT-HOOKS] DOM refs
   outside render; [REACT-ID] unique names; [WCAG22] modal focus boundaries.
   Neutral tokens start controls.css. Escape is native; close restores focus. */
import { useId, useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';
import './controls.css';

interface Props {
  /** Visible question used as the dialog's accessible name. */
  readonly question?: string;
}

export function ViewDialog({ question = 'Use the compact view?' }: Props) {
  const titleId = useId();
  const dialog = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLButtonElement>(null);
  const cancel = useRef<HTMLButtonElement>(null);
  const apply = useRef<HTMLButtonElement>(null);
  const [notice, setNotice] = useState('');

  function handleOpen() {
    dialog.current?.showModal();
    cancel.current?.focus();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLDialogElement>) {
    if (event.key !== 'Tab') return;
    // This fixed dialog has exactly two persistent enabled controls.
    // A dialog with dynamic content must compute its current Tab order.
    const boundary = event.shiftKey ? cancel.current : apply.current;
    if (event.currentTarget.ownerDocument.activeElement === boundary) {
      event.preventDefault();
      (event.shiftKey ? apply.current : cancel.current)?.focus();
    }
  }

  return (
    <div className="demo-panel">
      <button
        className="demo-button"
        type="button"
        ref={opener}
        onClick={handleOpen}
      >
        Open view chooser
      </button>
      <dialog
        className="demo-dialog"
        ref={dialog}
        aria-labelledby={titleId}
        onKeyDown={handleKeyDown}
        onClose={() => opener.current?.focus()}
      >
        <h2 id={titleId}>{question}</h2>
        <p>This example changes only the status below.</p>
        <div className="demo-row">
          <button
            className="demo-button"
            type="button"
            ref={cancel}
            onClick={() => dialog.current?.close()}
          >
            Cancel
          </button>
          <button
            className="demo-button"
            type="button"
            ref={apply}
            onClick={() => {
              setNotice('Compact view selected.');
              dialog.current?.close();
            }}
          >
            Apply view
          </button>
        </div>
      </dialog>
      <p role="status">{notice}</p>
    </div>
  );
}
