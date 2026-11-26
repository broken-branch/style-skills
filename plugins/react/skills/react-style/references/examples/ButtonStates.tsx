/* [REACT-RULES] pure rendering and functional updates; [REACT-LISTS] stable keys;
   [REACT-DOM] native disabled/busy controls. Neutral tokens start controls.css.
   data-preview illustrates states; keyboard focus still follows the real DOM. */
import { useState } from 'react';
import './controls.css';

const previews = ['default', 'hover', 'focus-visible', 'active'] as const;

export function ButtonStates() {
  const [activations, setActivations] = useState(0);

  return (
    <div className="demo-panel">
      <p>
        Hover, press or Tab to a button. Named previews illustrate each state.
      </p>
      <div className="demo-row">
        {previews.map((preview) => (
          <button
            className="demo-button"
            type="button"
            key={preview}
            data-preview={preview}
            onClick={() => setActivations((count) => count + 1)}
          >
            {preview}
          </button>
        ))}
        <button className="demo-button" type="button" disabled>
          Disabled
        </button>
        <button className="demo-button" type="button" disabled aria-busy="true">
          Loading…
        </button>
      </div>
      <p role="status">Activated {activations} times.</p>
    </div>
  );
}
