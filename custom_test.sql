\if (:client_id >> 201)
    \set aid random(500010, 510000)
    UPDATE sc_lakebase_demo.vehicle_ins_idx_big  
    SET name = 'U_' || name  
    WHERE insurance_no = :aid ;
\else
    \set bid random(500001, 4499999)
    SELECT name FROM sc_lakebase_demo.vehicle_ins_idx_big 
    WHERE insurance_no = :bid ;
\endif

 
