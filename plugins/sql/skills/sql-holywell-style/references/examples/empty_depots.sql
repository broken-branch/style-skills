/* [HOLYWELL-SQL] Subqueries, Spaces and Aliasing or correlations.
   Portable SQL; zero-quantity records still count as inventory. */
  SELECT d.depot_id, d.depot_name
    FROM depots AS d
   WHERE NOT EXISTS
         (SELECT i.item_id
            FROM inventory AS i
           WHERE i.depot_id = d.depot_id
         )
ORDER BY d.depot_id;
