### Question 2 
`docker run -it --entrypoint=bash python:3.9` 

### Question 3 to Question 6 
Prepare environment for PostgreSQL
1. Run command
	```
	python ingest_data_hw.py \
	--user=*** \
	--password=*** \
	--host=*** \
	--port=*** \
	--db=ny_taxi \
	--table_name=gree_tripdata \
	--url="[https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz)"
	```
2. Insert timezone data
	```Python
	user='***' 
	password='***'
	host='***'
	port=***
	db='ny_taxi'
	table_name='taxi_zone_lookup'
	url='https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
	
	engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
	data = pd.read_csv(r'/Users/louisekuo/Documents/04_DataEngineerZoomcamp/01-docker-terraform/01_docker/data/taxi+_zone_lookup.csv', index_col=None)
	data.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
	data.to_sql(name=table_name, con=engine, if_exists='append')
	```
3. Solutions
	```SQL
	-- Question 3. Count records
	SELECT count(*)
	FROM green_tripdata
	WHERE date(lpep_pickup_datetime) = date'2019-09-18'
	AND date(lpep_dropoff_datetime) = date'2019-09-18'
	;
	
	-- Question 4. Largest trip for each day
	SELECT lpep_pickup_datetime
	FROM green_tripdata
	WHERE trip_distance = (SELECT max(trip_distance) FROM green_tripdata)
	;
	
	-- Question 5. Three biggest pickups
	SELECT 
		b."Borough"
		, sum(a.total_amount) AS total_amount
	FROM green_tripdata a 
	JOIN taxi_zone_lookup b ON a."PULocationID" = b."LocationID"
	WHERE date(a.lpep_pickup_datetime) = date'2019-09-18'
	AND b."Borough" <> 'Unknown'
	GROUP BY 1
	ORDER BY 2 DESC 
	;
	
	-- Question 6. Largest tip
	SELECT 
		dropoff."Zone"
		, sum(a.tip_amount) AS ttl_tip_amount 
	FROM green_tripdata a 
	JOIN taxi_zone_lookup pickup ON a."PULocationID" = pickup."LocationID"
	JOIN taxi_zone_lookup dropoff ON a."DOLocationID" = dropoff."LocationID"
	WHERE 1=1 
	AND date_trunc('month', date(a.lpep_pickup_datetime)) = date'2019-09-01'
	AND pickup."Zone" = 'Astoria'
	AND dropoff."Zone" IN ('Central Park', 'Jamaica', 'JFK Airport', 'Long Island City/Queens Plaza')
	GROUP BY 1 
	ORDER BY 2 DESC 
	;
	```
