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

	# data is only available in parquet format now 
	parquet_name = 'output.parquet'
	os.system(f'wget {url} -O {parquet_name}')
	df = pd.read_parquet(parquet_name)

	csv_name = 'output.csv'
	df.to_csv(csv_name)

	engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

	df_tier = pd.read_csv(csv_name, iterator=True, chunksize=100000)
	df = next(df_tier)
	df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
	df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
	# First to create an empty table 
	df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace') 

	## Start inserting data by chunk
	while True:
		try: 
			t_start = time()

			df = next(df_tier)
			df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
			df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
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