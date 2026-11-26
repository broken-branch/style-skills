// House rules: narrow unknown inputs and preserve optional-property meaning
// [TS-CONFIG]; named exports and readonly structural contracts [GOOGLE-TS].

export interface Batch {
  readonly label: string;
  readonly count: number;
  readonly note?: string;
}

/** Validate an external record; ignore extra fields without copying them. */
export function parseBatch(value: unknown): Batch {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TypeError('A batch must be an object');
  }
  if (!('label' in value) || typeof value.label !== 'string') {
    throw new TypeError('A batch label must be text');
  }
  const label = value.label.trim();
  if (label.length === 0 || label.length > 80) {
    throw new RangeError('A batch label must contain 1 to 80 characters');
  }
  if (!('count' in value) || typeof value.count !== 'number') {
    throw new TypeError('A batch count must be a number');
  }
  const count = value.count;
  if (
    !Number.isFinite(count) ||
    !Number.isInteger(count) ||
    count < 0 ||
    count > 1000
  ) {
    throw new RangeError('A batch count must be an integer from 0 to 1000');
  }
  if ('note' in value) {
    if (typeof value.note !== 'string' || value.note.length > 200) {
      throw new TypeError(
        'A supplied batch note must be text of at most 200 characters',
      );
    }
    return { label, count, note: value.note };
  }
  return { label, count };
}
