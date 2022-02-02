 DO
$do$

DECLARE sql text;
        sql2 text;
        var text;
        var2 text;
BEGIN

EXECUTE 'SELECT setval(''messages_id_seq'', (SELECT max(id) FROM messages));';

sql2 := 'SELECT '' SELECT '' || array_to_string(ARRAY(SELECT ''m'' || ''.'' || c.column_name
        FROM information_schema.columns As c
            WHERE table_name = ''messages''
            AND  c.column_name NOT IN(''id'')
    ), '','') || '' FROM messages m'';';

—SELECT m.action_id,m.api_client_id,m.created_at,m.updated_at FROM messages

EXECUTE sql2 into var;

sql2 := 'SELECT  array_to_string(ARRAY(SELECT '' '' || c.column_name
        FROM information_schema.columns As c
            WHERE table_name = ''messages''
            AND  c.column_name NOT IN(''id'')),'','') || '''';';
— action_id, api_client_id, created_at, updated_at

EXECUTE sql2 into var2;

sql := 'INSERT INTO messages (' || var2|| ') ' || var || ';';

EXECUTE sql;
END;
$do$
;
