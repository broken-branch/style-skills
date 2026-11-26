/* [REACT-DOM] controlled inputs; [REACT-ID] reusable label/error relationships;
   [REACT-EFFECTS] derived validation and event-owned submission;
   [WCAG22] repairable errors and a native checkbox switch.
   Neutral tokens start controls.css. Submit empty, then correct the title. */
import { useId, useRef, useState } from 'react';
import type { SubmitEvent } from 'react';
import './controls.css';

export function PreferenceForm() {
  const id = useId();
  const titleInput = useRef<HTMLInputElement>(null);
  const [title, setTitle] = useState('');
  const [compact, setCompact] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [notice, setNotice] = useState('');
  const invalid = submitted && title.trim() === '';

  function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
    if (title.trim() === '') {
      setNotice('Preferences need a title.');
      titleInput.current?.focus();
      return;
    }
    setNotice('Preferences previewed. Nothing was saved.');
  }

  return (
    <div className="demo-panel">
      <form noValidate onSubmit={handleSubmit}>
        <div className="demo-field">
          <label htmlFor={`${id}-title`}>Item title (required)</label>
          <input
            className="demo-input"
            id={`${id}-title`}
            ref={titleInput}
            name="title"
            type="text"
            required
            value={title}
            onChange={(event) => {
              setTitle(event.currentTarget.value);
              setNotice('');
            }}
            aria-invalid={invalid}
            aria-describedby={`${id}-error`}
          />
          <p className="demo-error" id={`${id}-error`}>
            {invalid ? 'Error: enter an item title.' : ''}
          </p>
        </div>
        <label className="demo-switch">
          <input
            type="checkbox"
            role="switch"
            name="compact"
            checked={compact}
            onChange={(event) => setCompact(event.currentTarget.checked)}
          />
          Compact layout
        </label>
        <button className="demo-button" type="submit">
          Preview preferences
        </button>
      </form>
      <p role="status">{notice}</p>
    </div>
  );
}
