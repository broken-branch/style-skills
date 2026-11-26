/**
 * @fileoverview Google TypeScript: [prefer-interfaces] structural contracts;
 * [any-unknown] narrow opaque input; [exception-handling] throw on failure;
 * [exports] named exports.
 */

/** A label's stable identity and user-visible text. */
export interface LabelRecord {
  readonly id: string;
  readonly text: string;
}

/** Checks an untrusted value without asserting its shape. */
export function parseLabelRecord(value: unknown): LabelRecord {
  if (typeof value !== 'object' || value === null ||
      !('id' in value) || typeof value.id !== 'string' ||
      !('text' in value) || typeof value.text !== 'string' ||
      value.id.length === 0) {
    throw new TypeError('A label needs a nonempty id and string text.');
  }
  return {id: value.id, text: value.text};
}
