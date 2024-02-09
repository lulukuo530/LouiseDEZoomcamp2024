-- Question 1: What is count of records for the 2022 Green Taxi Data??
SELECT count(*) 
FROM `groovy-ace-412002.ny_taxi.green_tax_data_2022`
;

-- Question 2. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
SELECT distinct PULocationIDs
FROM `groovy-ace-412002.ny_taxi.green_tax_data_2022`
;

-- Question 3. How many records have a fare_amount of 0?
SELECT count(*) 
FROM `groovy-ace-412002.ny_taxi.green_tax_data_2022`
WHERE fare_amount = 0 
;

-- Question 5. Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
SELECT distinct PULocationIDs
FROM `groovy-ace-412002.ny_taxi.green_tax_data_2022`
WHERE date(lpep_pickup_datetime) >= date'2022-06-01'
AND date(lpep_pickup_datetime) <= date'2022-06-30'
;
