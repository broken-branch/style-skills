/**
 * @fileoverview Google TypeScript: [no-private-fields] TypeScript privacy;
 * [use-readonly] fixed field binding; [arrayt-type] simple array notation;
 * [visibility] omit public; [function-declarations] named helper declaration.
 */

/** Owns pending labels and exposes detached snapshots for display. */
export class LabelQueue {
  private readonly labels: string[] = [];

  /** Appends a nonblank label, discarding surrounding whitespace. */
  add(label: string): void {
    this.labels.push(normalizeLabel(label));
  }

  /** Removes the oldest label, or returns undefined when empty. */
  take(): string | undefined {
    return this.labels.shift();
  }

  /** Returns a copy that cannot expose the queue's mutable storage. */
  snapshot(): readonly string[] {
    return [...this.labels];
  }
}

function normalizeLabel(label: string): string {
  const normalized = label.trim();
  if (normalized.length === 0) {
    throw new RangeError('A queued label must contain visible text.');
  }
  return normalized;
}
