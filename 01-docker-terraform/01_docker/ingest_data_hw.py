import os 
import argparse 
import pandas as pd 
from time import time 
from sqlalchemy import create_engine


def main(params):
	user = params.user
	password = params.password
	host = params.host 
	port = params.port 
	db = params.db
	table_name = params.table_name 
	url = params.url 

	# the backup files are gzipped, and it's important to keep the correct extension
	# for pandas to be able to open the file
	if url.endswith('.csv.gz'):
			csv_name = 'output.csv.gz'
	else:
			csv_name = 'output.csv'

	os.system(f"wget {url} -O {csv_name}")

	engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

	df_tier = pd.read_csv(csv_name, iterator=True, chunksize=100000)
	df = next(df_tier)
	# df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
	# df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
	# First to create an empty table 
	df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace') 

	## Start inserting data by chunk
	while True:
		try: 
			t_start = time()

			df = next(df_tier)
			# df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
			# df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
			df.to_sql(name=table_name, con=engine, if_exists='append') 

			t_end = time()

			print('inserting another chunk, took %.3f seconds' % (t_end - t_start))

		except StopIteration:
			print('Finished ingesting data into the postgres database')
			break


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

	parser.add_argument('--user', required=True, help='username for postgres')
	parser.add_argument('--password', required=True, help='password for postgres')
	parser.add_argument('--host', required=True, help='host for postgres')
	parser.add_argument('--port', required=True, help='port for postgres')
	parser.add_argument('--db', required=True, help='database name for postgres')
	parser.add_argument('--table_name', required=True, help='table name for postgres')
	parser.add_argument('--url', required=True, help='url of the csv file')

	args = parser.parse_args()

	main(args)
	

"""
python ingest_data_hw.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=gree_tripdata \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
"""

### for timezone data 
# user='root' 
# password='root'
# host='localhost'
# port=5433 
# db='ny_taxi'
# table_name='taxi_zone_lookup'
# url='https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'

# engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
# data = pd.read_csv(r'/Users/louisekuo/Documents/04_DataEngineerZoomcamp/01-docker-terraform/01_docker/data/taxi+_zone_lookup.csv', index_col=None)
# data.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
# data.to_sql(name=table_name, con=engine, if_exists='append')
### 