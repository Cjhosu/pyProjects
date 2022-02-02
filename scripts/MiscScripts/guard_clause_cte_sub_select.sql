WITH parameter_indicators_insert_cte AS (
    INSERT INTO somewhere (parameter_id, indicator_id, required, priority, created_at, updated_at)
    SELECT
           id
           ,(SELECT id FROM select_table WHERE value = 'User Value')
           ,true
           ,1
           ,CURRENT_TIMESTAMP
           ,CURRENT_TIMESTAMP
      FROM parameters
     WHERE NOT EXISTS (
                       SELECT 'x'
                         FROM  table_value tv
                        WHERE parameter = '<parameter>'
                      )
    RETURNING id
) SELECT id INTO rollback.sample_rb FROM sampe_cte;
