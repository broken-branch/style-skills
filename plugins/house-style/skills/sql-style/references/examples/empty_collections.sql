-- House rules: correlated NOT EXISTS and explicit outer references [PG-PITFALLS]
-- [GITLAB-SQL]; stable limited output with a unique tie-breaker [SQLFLUFF].
-- Grain: up to 20 newest collections without any artifacts, regardless of age.
-- collection_id is non-null on both sides; the subquery cannot lose NULL keys.
SELECT
  collections.collection_id,
  collections.collection_name,
  collections.created_at
FROM artifact_collections AS collections
WHERE
  NOT EXISTS (
    SELECT artifacts.artifact_id
    FROM artifacts
    WHERE artifacts.collection_id = collections.collection_id
  )
ORDER BY collections.created_at DESC, collections.collection_id DESC
LIMIT 20;
