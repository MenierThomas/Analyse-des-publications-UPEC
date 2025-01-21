from pyspark.sql import SparkSession

def run_pyspark_task():
    spark = SparkSession.builder \
        .appName("Django PySpark SQLite Example") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .getOrCreate()

    df = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite") \
        .option("dbtable", "hal") \
        .option("driver", "org.sqlite.JDBC") \
        .load()
    
    df.show()

    return df.collect()


# def run_pyspark_task():
#     # Initialize PySpark with SQLite JDBC driver
#     spark = SparkSession.builder \
#         .appName("Django PySpark SQLite Example") \
#         .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \
#         .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow") \
#         .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/myapp/sqlite-jdbc-3.48.0.0.jar").getOrCreate()

#     # SQLite Database URL
#     jdbc_url = "jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite"  # Path to your SQLite database file

#     # Step 1: Read data from SQLite into a DataFrame
#     query = "(SELECT * FROM hal) AS users_table"  # Example query to select data from the SQLite table
#     df_from_sqlite = spark.read \
#         .format("jdbc") \
#         .option("url", jdbc_url) \
#         .option("dbtable", query) \
#         .load()

#     # Show the data read from SQLite
#     df_from_sqlite.show()

#     # # Example DataFrame
#     # data = [("Alice", 30), ("Bob", 25), ("Cathy", 35)]
#     # columns = ["Name", "Age"]
#     # df = spark.createDataFrame(data, columns)

#     # # Perform a transformation on the DataFrame
#     # df_filtered = df.filter(df.Age > 28)

#     # # Collect the result as a Python list
#     # result = df_filtered.collect()

#     # Step 2: Write the transformed data to SQLite (e.g., into a new table or append to existing)
#     # df_filtered.write \
#     #     .format("jdbc") \
#     #     .option("url", jdbc_url) \
#     #     .option("dbtable", "filtered_users")  # The table where the data will be written
#     #     .mode("overwrite")  # You can use "append" if you want to add to the existing table
#     #     .save()

#     # Stop the Spark session
#     spark.stop()

#     return df_from_sqlite.collect()  # Return the collected data from SQLite
