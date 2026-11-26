/* Airbnb React/JSX: [airbnb-react-jsx:6] named stateless function;
   [airbnb-react-jsx:19] JSX/JS quotes; [airbnb-react-jsx:29] modern defaults.
   React 19 uses parameter defaults instead of function defaultProps. */
import React from 'react';

/** @param {{label: string, isPending?: boolean}} props */
export default function StatusBadge({ label, isPending = false }) {
  return (
    <span
      className="status-badge"
      role="status"
      aria-busy={isPending}
    >
      {isPending ? 'Waiting: ' : 'Ready: '}{label}
    </span>
  );
}
