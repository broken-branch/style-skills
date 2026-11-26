// House rules: discriminated unions and readonly contracts [GOOGLE-TS];
// unknown rejection values and handled promises [TS-CONFIG] [TS-ESLINT].

export interface Success<Value> {
  readonly status: 'success';
  readonly value: Value;
}

export interface Failure {
  readonly status: 'failure';
  readonly error: Error;
}

export type Result<Value> = Success<Value> | Failure;

/** Capture an adapter failure for an internal caller that handles both variants. */
export async function captureResult<Value>(
  operation: () => Promise<Value>,
): Promise<Result<Value>> {
  try {
    return { status: 'success', value: await operation() };
  } catch (cause: unknown) {
    const error =
      cause instanceof Error
        ? cause
        : new Error('The adapter failed with a non-Error value', { cause });
    return { status: 'failure', error };
  }
}
