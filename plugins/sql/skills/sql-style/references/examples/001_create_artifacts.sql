-- House rules: identity keys and named relational constraints [PG-CONSTRAINTS];
-- instant timestamps [PG-PITFALLS] and bounded migration locks [PG-LOCK-TIMEOUT].
-- First migration only: both tables are new. Run with psql -X -v ON_ERROR_STOP=1.
-- Choose the lock budget for deployment. On failure, roll back before retrying.
BEGIN;
SET LOCAL lock_timeout = '3s';

CREATE TABLE artifact_collections (
  collection_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  collection_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT artifact_collections_name_check CHECK (LENGTH(TRIM(collection_name)) > 0)
);

CREATE TABLE artifacts (
  artifact_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  collection_id BIGINT NOT NULL,
  byte_count BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT artifacts_collection_fk FOREIGN KEY (collection_id)
  REFERENCES artifact_collections (collection_id),
  CONSTRAINT artifacts_byte_count_check CHECK (byte_count >= 0)
);

COMMIT;
