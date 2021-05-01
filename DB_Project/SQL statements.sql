--#1
SELECT make_name,first_year FROM brands ORDER BY first_year ASC;

--#2
SELECT model_name, vehicle_type FROM models WHERE vehicle_type = "truck" or vehicle_type = "mpv";

--#3
SELECT make_name, COUNT(model_id) FROM models INNER JOIN brands ON brands.make_id =  models.make_id GROUP BY make_name;

--#4
SELECT model_name as Model,make_name as Brand FROM models INNER JOIN brands ON brands.make_id =  models.make_id;

--#5
SELECT A.make_name As Name1, B.make_name AS Name2, A.first_year FROM brands A, brands B
WHERE A.make_id <> B.make_id AND A.first_year = B.first_year 
ORDER BY A.first_year; 

--#6
SELECT brands.make_name, brands.make_id,models.model_name, models.make_id
FROM brands
INNER JOIN models ON brands.make_id = models.make_id
UNION ALL
SELECT brands.make_name, brands.make_id,cast(NULL as varchar(20)), cast(NULL as integer)
FROM brands 
WHERE NOT EXISTS (
    SELECT * FROM models WHERE brands.make_id = models.make_id)
UNION ALL
SELECT cast(NULL as varchar(50)), cast(NULL as integer), models.model_name, models.make_id
FROM models
WHERE NOT EXISTS (
    SELECT * FROM brands WHERE brands.make_id = models.make_id)

--#7
SELECT make_name from brands WHERE make_id IN (SELECT make_id from models where vehicle_type = "truck")

--#8
SELECT make_id FROM brands UNION SELECT make_id FROM models ORDER BY make_id;





