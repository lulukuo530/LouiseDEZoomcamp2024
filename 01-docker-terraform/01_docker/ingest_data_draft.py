import pandas as pd 
from sqlalchemy import create_engine

data = pd.read_csv(r'yellow_tripdata_2021-01.csv', nrows=100)
data.tpep_pickup_datetime = pd.to_datetime(data.tpep_pickup_datetime)
data.tpep_dropoff_datetime = pd.to_datetime(data.tpep_dropoff_datetime)
print(pd.io.sql.get_schema(data, name = 'yellow_taxi_data'))

engine = create_engine('postgresql://root:root@localhost:5433/ny_taxi')
# engine.connect()

df_tier = pd.read_csv(r'yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)
df = next(df_tier)
len(df)
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
# First to create an empty table 
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace') 
# Start inserting data by first tier 
df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append') 

## Start inserting data by chunk
from time import time 
while True:
	t_start = time()

	df = next(df_tier)
	df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
	df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
	df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append') 

	t_end = time()

	print('inserting another chunk, took %.3f seconds' % (t_end - t_start))