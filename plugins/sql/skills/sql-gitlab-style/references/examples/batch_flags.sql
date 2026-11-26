/* [GITLAB-SQL] Functions and Naming Conventions: IFF, IFNULL, is_ names.
   Original Snowflake query; NULL units are treated as zero and never urgent. */
SELECT
  batch_id,
  IFNULL(pending_units, 0)                        AS pending_units,
  IFF(IFNULL(pending_units, 0) > 10, TRUE, FALSE) AS is_urgent
FROM batches
ORDER BY batch_id;
