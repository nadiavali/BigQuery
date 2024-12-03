# Export credential first
from google.cloud import bigquery

# Create client object
client = bigquery.Client()

# Constructe a ref to the openqa dataset
dataset_ref = client.dataset("openaq", project="bigquery-public-data")
# API req-  fetch dataset
dataset = client.get_dataset(dataset_ref)

#list all tables in openqa dataset
tables = list(client.list_tables(dataset))


# prints all the name of the tables in openqa(global_air_quality)
for table in tables:
    print(table.table_id)


# Constructe a ref to global_air_quality table
table_ref = dataset_ref.table("global_air_quality")

# API req, fetch table
table = client.get_table(table_ref)

# perview first fim´ve lines of global_air_quality table
info = client.list_rows(table, max_results=5).to_dataframe()
print(info)


# Query select all items from city where country is US

# query = """
# SELECT city
# FROM `bigquery-public-data.openaq.global_air_quality`
# WHERE country = 'US'
# """

query = """
        SELECT *
        FROM `bigquery-public-data.openaq.global_air_quality`
        WHERE country = 'US'
        """

query_job = client.query(query)
us_Cities = query_job.to_dataframe()
#print(us_Cities)
# What five cities have the most measurements?
print(us_Cities.city.value_counts().head())


# Query to select countries with units of "ppm"
first_query = """
SELECT country
FROM `bigquery-public-data.openaq.global_air_quality`
WHERE unit = 'ppm'
""" # Your code goes here

# Set up the query (cancel the query if it would use too much of 
# your quota, with the limit set to 10 GB)
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
first_query_job = client.query(first_query, job_config=safe_config)

# API request - run the query, and return a pandas DataFrame
first_results = first_query_job.to_dataframe()

# View top few rows of results
print(first_results.head())




# Query to select all columns where pollution levels are exactly 0
zero_pollution_query = """
SELECT *
FROM `bigquery-public-data.openaq.global_air_quality`
WHERE value = 0.0
""" # Your code goes here

# Set up the query
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)
query_job = client.query(zero_pollution_query, job_config=safe_config)

# API request - run the query and return a pandas DataFrame
zero_pollution_results = query_job.to_dataframe() # Your code goes here

print(zero_pollution_results.head())