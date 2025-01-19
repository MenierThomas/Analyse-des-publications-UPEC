from pyspark.sql import SparkSession
from pyspark_ai import SparkAI

# Initialize Spark session
spark = SparkSession.builder \
    .appName("PySparkAIQuery") \
    .config("spark.master", "local") \
    .getOrCreate()

# Initialize PySparkAI with OpenAI API Key
spark_ai = SparkAI(
    spark_session=spark,
    openai_api_key="YOUR_OPENAI_API_KEY"  # Replace with your OpenAI key
)

def query_sqlite(query):
    """
    Use PySparkAI to query the SQLite database.
    :param query: Natural language query.
    :return: Query result as a DataFrame.
    """
    # Read SQLite database into Spark DataFrame
    sqlite_path = "db.sqlite"  # Adjust the path if necessary
    table_name = "hal"  # Replace with the actual table name

    # Load the SQLite database into Spark
    df = spark.read.format("jdbc") \
        .option("url", f"jdbc:sqlite:{sqlite_path}") \
        .option("dbtable", table_name) \
        .option("driver", "org.sqlite.JDBC") \
        .load()

    # Use PySparkAI to execute the natural language query
    result_df = spark_ai.sql(query, df)

    return result_df
