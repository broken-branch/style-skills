-- [GITLAB-SQL] Best Practices and Reference Conventions: != and LOWER/LIKE.
-- Original portable query; one row per matching batch, ordered by its key.
SELECT
  batch_id,
  batch_name
FROM batches
WHERE
  batch_status != 'closed'
  AND LOWER(batch_name) LIKE 'sample%'
ORDER BY batch_id;
