watch "psql -c \"select usename, client_addr, count from pg_stat_activity where usename like '%service_name%' group by usename, client_addr order by client_addr;\""
