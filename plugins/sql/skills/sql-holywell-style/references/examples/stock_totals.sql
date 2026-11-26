/* [HOLYWELL-SQL] Uniform suffixes, Spaces and Preferred formalisms.
   Portable SQL; report each depot's available quantity, including zero totals. */
  SELECT i.depot_id,
         COUNT(*) AS item_tally,
         SUM(CASE i.stock_status
                 WHEN 'available' THEN i.quantity_num
                 ELSE 0
             END) AS available_total
    FROM inventory AS i
GROUP BY i.depot_id
ORDER BY i.depot_id;
