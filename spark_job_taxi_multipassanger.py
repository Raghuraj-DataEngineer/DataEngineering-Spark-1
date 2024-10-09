# %% [markdown]
# ## Data discovery: Load and query Yellow Taxi data
# > Download the dataset from [the official TLC Trip Record Data website](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
from pyspark.sql import SparkSession

# %%
# Create SparkSession
spark = SparkSession.builder\
             .master("local[1]")\
             .appName("spark-app-version-x")\
             .getOrCreate()

# %%
# Read taxi data. These can be input parameters, using python arguments.
input_path = 'production_data/yellow_taxis/'
output_path = 'reporting/etl_job_taxis_multi_passanger_trips/'

# %%
# Load data into Spark dataframe
df = spark.read.parquet(input_path)

# %%
# Query sample, using Spark SQL
df.createOrReplaceTempView('tbl_raw_yellow_taxis')

# %%
# SQL Statement
df_output = spark.sql('''
                        SELECT VendorID, tpep_pickup_datetime, passenger_count 
                        FROM tbl_raw_yellow_taxis 
                        WHERE total_amount > 1 
                          AND passenger_count > 2
                        ''')

# %%
# Write data to output
df_output.write.mode('overwrite').parquet(output_path)

# %%
# Stop the session
spark.stop()




