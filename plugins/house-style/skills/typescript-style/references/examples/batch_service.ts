// House rules: type-only imports and emitted ESM paths [TS-CONFIG];
// return await and exhaustive discriminated-union handling [TS-ESLINT].

import { parseBatch } from './batch.js';
import type { Batch } from './batch.js';
import { captureResult } from './result.js';
import type { Result } from './result.js';

/** Load through an injected adapter, validating its untrusted result. */
export async function loadBatch(
  read: () => Promise<unknown>,
): Promise<Result<Batch>> {
  return await captureResult(async () => parseBatch(await read()));
}

/** Describe the outcome without exposing adapter diagnostics to a caller. */
export function describeBatch(result: Result<Batch>): string {
  switch (result.status) {
    case 'success':
      return `${result.value.label}: ${result.value.count} items`;
    case 'failure':
      return 'The batch could not be loaded';
  }
}
