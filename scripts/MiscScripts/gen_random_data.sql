DO
$$
DECLARE counter int;
BEGIN
    counter:=0;
    WHILE counter < 100000
    LOOP
        BEGIN
            INSERT INTO rxr_load_alternatives
            (rxservice_prescription_id, event, created_at, updated_at)
            VALUES
            ((SELECT floor(random()*(20000-10000+1))+10000),  '{"ddid": "002765", "alternatives": [{"ddid": "111111", "tier": "Tier 1", "ranking": 1, "drug_name": "Cliff Bars"}, {"ddid": "111112", "tier": "Tier 2", "ranking": 2, "drug_name": "House Jamz"}, {"ddid": "111113", "tier": "Tier 3", "ranking": 3, "drug_name":"Snack Crackers"}, {"ddid": "111114", "tier": "Tier 4", "ranking": 4, "drug_name": "Chicken"}, {"ddid": "111115", "tier": "Tier 5", "ranking": 5, "drug_name": "Bacon"}]}', timeofday()::timestamptz, timeofday()::timestamptz);
            counter := counter +1 ;
        END;
    END LOOP;
END;
$$

DO
$$
DECLARE counter int;
BEGIN
    counter:=0;
    WHILE counter < 1000
    LOOP
        BEGIN
            INSERT INTO rxr_submissions
            (rxservice_prescription_id, event, created_at, updated_at)
            VALUES
            ((SELECT la.rxservice_prescription_id FROM rxr_load_alternatives la LEFT JOIN rxr_submissions sub ON la.rxservice_prescription_id = sub.rxservice_prescription_id WHERE sub.rxservice_prescription_id IS NULL ORDER BY random() limit 1), '{"note": "pick this one", "alternatives": {"prescription_alternatives": [{"drug_name": "Chicken"}, {"drug_name": "Bacon", "recommended": "true"}, {"drug_name": "Cliff Bars"}, {"drug_name": "Cold Brew Coffee", "recommended": "true"}, {"drug_name": "Cheeseburgers"}]}}' , timeofday()::timestamptz, timeofday()::timestamptz);
            counter := counter +1 ;
        END;
    END LOOP;
END;
$$
;
