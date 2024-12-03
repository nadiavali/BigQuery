from google.cloud import bigquery


# First step: Create a "Client" object
# Client object will play a central role in retrieving information from BigQuery datasets.
# It allows to execute API requests like fetching datasets, listing tables, and retrieving rows.
client = bigquery.Client()


# Construct a reference to the "hacker_news" dataset
# client.dataset creates a reference to the hacker_news dataset within the bigquery-public-data project.
dataset_ref = client.dataset("hacker_news", project="bigquery-public-data")

# API request - fetch the dataset
# fetches metadata about the dataset
# A dataset reference is required to list its tables or query its contents.

dataset = client.get_dataset(dataset_ref)

# list all the tables in the hacker_news dataset
tables = list(client.list_tables(dataset))

# Print names of all tables in the dataset
for table in tables:
    print(table.table_id)

# Construct a reference to the "full" table
table_ref = dataset.table("full")
table = client.get_table(table_ref) # full


# Each SchemaField tells us about a specific column (which we also refer to as a field)
schema = table.schema
for field in schema:
    print(field)
    #print(f"Name: {field.name}, Type: {field.field_type}, Mode: {field.mode}")


'''We can use the list_rows() method to check just the first five lines 
of of the full table to make sure this is right. (Sometimes databases have
outdated descriptions, so it's good to check.) This returns a BigQuery
RowIterator object that can quickly be converted to a pandas DataFrame with the to_dataframe() method'''
rows = client.list_rows(table, max_results=5).to_dataframe()
print(rows)


# rowss = client.list_rows(
#     table,
#     selected_fields=[
#         bigquery.SchemaField("text", "STRING"),
#         bigquery.SchemaField("by", "STRING"),
#         bigquery.SchemaField("time", "INTEGER"),
#     ],
#     max_results=5
# ).to_dataframe()

# print(rowss)

# # Preview the first five entries in the "by" column of the "full" table
# rows1 = client.list_rows(table, selected_fields=table.schema[:1], max_results=5).to_dataframe()
# print(rows1)


query =  """
SELECT text, `by`, TIMESTAMP_SECONDS(time) as timestamp
FROM `bigquery-public-data.hacker_news.full`
WHERE text IS NOT NULL
LIMIT 6
"""
query_job = client.query(query)
results = query_job.to_dataframe()
print(results)


#big-341@helpful-binder-443511-s6.iam.gserviceaccount.com