WITH codes_array AS (
select id
       ,claim #>> '{reject_codes}' as reject_codes
  from claims
)
Select id as claim_id, code_vals
FROM codes_array, json_array_elements(reject_codes::json) as code_val
