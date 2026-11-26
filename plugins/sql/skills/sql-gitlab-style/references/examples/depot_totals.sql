/* [GITLAB-SQL] Common Table Expressions, Aggregations, Reference Conventions.
   Original query; aggregate before the join to keep one row per depot.
   A depot with no batches has batch_count zero. */
WITH counted AS (
  SELECT
    depot_id,
    COUNT(*) AS batch_count
  FROM batches
  GROUP BY depot_id
)

SELECT
  depots.depot_id,
  depots.depot_name,
  IFNULL(counted.batch_count, 0) AS batch_count
FROM depots
LEFT JOIN counted
  ON depots.depot_id = counted.depot_id
ORDER BY depots.depot_id;
