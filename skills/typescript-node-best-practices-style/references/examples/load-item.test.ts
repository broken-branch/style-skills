/* Node.js Best Practices: [2.8] failure paths; [4.2] three-part test names;
   [4.3] arrange/act/assert; [4.5] per-test data; [6.27] node: imports.
   Run: node --test load-item.test.ts on a runtime with TS type stripping. */
import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { AppError, handleFailure } from './app-error.ts';
import { loadItem } from './load-item.ts';
import type { Item } from './load-item.ts';

// Named test bodies are callbacks, not global application state.
const returnsItem = async () => {
  const item: Item = { id: 'entry-4', title: 'Seeds' };
  const repository = { find: async (_id: string) => item };

  const result = await loadItem(item.id, repository);

  assert.deepEqual(result, item);
};
test('loadItem: existing ID: returns the stored item', returnsItem);

const missingItem = async () => {
  const repository = { find: async (_id: string) => undefined };

  const result = loadItem('absent', repository);

  await assert.rejects(result, {
    name: 'AppError', code: 'ITEM_NOT_FOUND', isOperational: true,
  });
};
test('loadItem: missing ID: exposes an operational error', missingItem);

const failedRead = async () => {
  const failure = new Error('Storage unavailable');
  const repository = { find: async (_id: string) => { throw failure; } };

  const result = loadItem('entry-9', repository);

  await assert.rejects(result, failure);
};
test('loadItem: repository rejects: preserves the failure', failedRead);

const recoverableError = () => {
  const failure = new AppError('ITEM_NOT_FOUND', 'Unavailable', true);
  const records: object[] = [];
  const logger = { error: (fields: object) => { records.push(fields); } };

  const decision = handleFailure(failure, logger);

  assert.equal(decision, 'continue');
  assert.deepEqual(records, [{ code: 'ITEM_NOT_FOUND', operational: true }]);
};
test('handleFailure: known operational error: continues', recoverableError);

const unknownError = () => {
  const records: object[] = [];
  const logger = { error: (fields: object) => { records.push(fields); } };

  const decision = handleFailure('untrusted diagnostic text', logger);

  assert.equal(decision, 'restart');
  assert.deepEqual(records, [{ code: 'UNEXPECTED_FAILURE', operational: false }]);
};
test('handleFailure: unknown failure: requests restart without leaking it', unknownError);
