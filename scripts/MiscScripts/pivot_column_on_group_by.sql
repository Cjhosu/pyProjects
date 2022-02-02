select 
color
,array_agg(name) as names
 from cats 
group by color
order by color desc

