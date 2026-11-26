-- House rules: index referencing keys [PG-CONSTRAINTS]; concurrent index DDL
-- outside transactions [PG-CREATEINDEX] and bounded waits [PG-LOCK-TIMEOUT].
-- Follow 001_create_artifacts.sql; this also permits writes if rows now exist.
-- Run in a dedicated psql -X -v ON_ERROR_STOP=1 -f session, without --single-transaction.
-- On failure, inspect pg_index for an invalid index; drop that invalid index
-- with DROP INDEX CONCURRENTLY before retrying. The failed session must close.
SET lock_timeout = '3s';

CREATE INDEX CONCURRENTLY artifacts_collection_id_idx
ON artifacts (collection_id);

RESET lock_timeout;
