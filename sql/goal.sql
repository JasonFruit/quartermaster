insert into item (
    condition_id,
    item,
    weight,
    weight_unit_id,
    life,
    life_unit_id,
    record_type_id,
    purchase_date)
select condition_id,
item,
cast(weight * ? as integer),
weight_unit_id,
life,
life_unit_id,
2,
null
from item i
inner join recordtype rt
on i.record_type_id = rt.id
where rt.description = 'recommendation';
