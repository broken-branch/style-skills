-- House rules: staged CTEs [PG-WITH], explicit qualified joins [GITLAB-SQL],
-- half-open instant windows and meaningful NULL fallbacks [PG-PITFALLS].
-- Bind $1 = inclusive start and $2 = exclusive end as TIMESTAMPTZ via a driver.
-- Grain: one row per collection, including collections with no matching artifact.
-- Aggregate before joining: each collection matches at most one totals row.
WITH recent_artifacts AS (
  SELECT
    collection_id,
    byte_count
  FROM artifacts
  WHERE
    created_at >= $1
    AND created_at < $2
),

collection_totals AS (
  SELECT
    collection_id,
    COUNT(*) AS artifact_count,
    SUM(byte_count) AS total_bytes
  FROM recent_artifacts
  GROUP BY collection_id
)

SELECT
  collections.collection_id,
  collections.collection_name,
  COALESCE(collection_totals.artifact_count, 0) AS artifact_count,
  COALESCE(collection_totals.total_bytes, 0) AS total_bytes
FROM artifact_collections AS collections
LEFT JOIN collection_totals
  ON collections.collection_id = collection_totals.collection_id
ORDER BY collections.collection_id;
