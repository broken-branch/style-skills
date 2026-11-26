/* Node.js Best Practices: [2.2] Error subclass with classification;
   [2.3] operational versus unknown failures; [2.4] central handling.
   The caller supplies a structured logger and drains/exits on "restart". */
export class AppError extends Error {
  readonly code: string;
  readonly isOperational: boolean;

  constructor(code: string, message: string, isOperational: boolean) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.isOperational = isOperational;
  }
}

export interface FailureLogger {
  error(fields: { code: string; operational: boolean }, message: string): void;
}

// Diagnostics deliberately omit the raw error, which may contain secrets.
export const handleFailure = (
  error: unknown,
  logger: FailureLogger,
): 'continue' | 'restart' => {
  const operational = error instanceof AppError && error.isOperational;
  logger.error(
    { code: operational ? error.code : 'UNEXPECTED_FAILURE', operational },
    'Operation failed',
  );
  return operational ? 'continue' : 'restart';
};
