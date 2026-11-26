/* Rules of React: [rules-of-react:16] immutable Hook arguments;
   [rules-of-react:17] immutable Hook results; [rules-of-react:25] fixed Hook.
   Call at component top level. Items have unique string IDs and stay immutable. */
import { useState } from 'react';

export function usePinnedItems(items) {
  const [pinnedIds, setPinnedIds] = useState([]);
  const pinnedItems = items.filter((item) => pinnedIds.includes(item.id));

  function togglePin(id) {
    setPinnedIds((current) => (
      current.includes(id)
        ? current.filter((candidate) => candidate !== id)
        : [...current, id]
    ));
  }

  return { pinnedItems, togglePin };
}
