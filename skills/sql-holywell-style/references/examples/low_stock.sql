/* [HOLYWELL-SQL] Spaces, Joins, Aliasing or correlations, Preferred formalisms.
   Portable SQL; quantity bounds are inclusive. One row per stock record. */
  SELECT i.item_id, i.item_name,
         d.depot_name, i.quantity_num
    FROM inventory AS i
         INNER JOIN depots AS d
         ON i.depot_id = d.depot_id
   WHERE i.quantity_num BETWEEN 1 AND 4
     AND i.stock_status IN ('available', 'reserved')
ORDER BY i.quantity_num, i.item_id;
