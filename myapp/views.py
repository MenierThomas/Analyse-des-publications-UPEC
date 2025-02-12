# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
# from .pyspark_ai import query_sqlite  # Import from pyspark_ai.py
from .pyspark_code import run_pyspark_task
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
=======
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year
import time
import matplotlib.pyplot as plt
import io
import base64
import zipfile
import pandas as pd
from django.http import HttpResponse
import os
>>>>>>> Stashed changes
>>>>>>> Stashed changes


def main_page(request):
    return render(request, 'myapp/main_page.html')


def pyspark_view(request):
    # Run PySpark task and get results
    results = run_pyspark_task()
<<<<<<< Updated upstream

    if results is None:
        return JsonResponse({"error": "No results found"}, status=500)
    
    # Get the first 20 rows (or all if needed)
    first_20_results = results[:20]  # Adjust this if you want more rows

    # Convert the results into a list of dictionaries
    # Each row is a dictionary where keys are column names
    formatted_results = [row.asDict() for row in first_20_results]

    return render(request, "myapp/pyspark_page.html", {"results": formatted_results})

# def query_db_view(request):
#     query = request.GET.get("query", "")
#     if not query:
#         return JsonResponse({"error": "No query provided"}, status=400)

#     try:
#         # Execute the PySpark AI query
#         result_df = query_sqlite(query)

#         # Collect result into a list of dictionaries
#         results = result_df.toPandas().to_dict(orient="records")

#         return JsonResponse({"results": results}, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
=======
<<<<<<< Updated upstream

    if results is None:
        return JsonResponse({"error": "No results found"}, status=500)
    
    # Get the first 20 rows (or all if needed)
    first_20_results = results[:20]  # Adjust this if you want more rows

    # Convert the results into a list of dictionaries
    # Each row is a dictionary where keys are column names
    formatted_results = [row.asDict() for row in first_20_results]

    return render(request, "myapp/pyspark_page.html", {"results": formatted_results})

# def query_db_view(request):
#     query = request.GET.get("query", "")
#     if not query:
#         return JsonResponse({"error": "No query provided"}, status=400)

#     try:
#         # Execute the PySpark AI query
#         result_df = query_sqlite(query)

#         # Collect result into a list of dictionaries
#         results = result_df.toPandas().to_dict(orient="records")

#         return JsonResponse({"results": results}, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
=======

    if results is None:
        return JsonResponse({"error": "No results found"}, status=500)
    
    # Get the first 20 rows (or all if needed)
    first_20_results = results[:20]  # Adjust this if you want more rows

    # Convert the results into a list of dictionaries
    # Each row is a dictionary where keys are column names
    formatted_results = [row.asDict() for row in first_20_results]

    return render(request, "myapp/pyspark_page.html", {"results": formatted_results})


def benchmark_view(request):
    # 1. Configuration PySpark
    spark = SparkSession.builder \
        .appName("Benchmark Tests") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .master("local[*]") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()

    # 2. Charger une base de données
    # Assurez-vous d'avoir une base configurée
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite",
        driver="org.sqlite.JDBC",
        dbtable="hal"
    ).load()

    # 3. Définir les benchmarks
    results = []
    cores = [1, 2, 4]  # Nombre de cœurs
    queries = {
        "domain_per_year": lambda df: df.filter((col("year") >= 2022))
                            .groupBy("domaine")
                            .count()
                            .orderBy(col("count").desc())
                            .show(),
        "publications_per_year": lambda df: df.withColumn("year", col("year")) \
                                            .groupBy("year") \
                                            .count() \
                                            .orderBy(col("year").asc()),
        "top_domains_by_year": lambda df: df.withColumn("year", col("year")) \
                                            .groupBy("year", "domaine") \
                                            .count() \
                                            .orderBy(col("year").asc(), col("count").desc()),
        "domains_no_publications_since": lambda df: df.filter(col("year") < 2020) \
                                                    .select("domaine") \
                                                    .distinct(),
        "average_publications_per_domain": lambda df: df.groupBy("domaine") \
                                                    .count() \
                                                    .agg({"count": "avg"}),
        "most_active_authors": lambda df: df.groupBy("author") \
                                            .count() \
                                            .orderBy(col("count").desc()) \
                                            .limit(10),
        "domains_in_year_range": lambda df: df.filter((col("year") >= 2015) & (col("year") <= 2020)) \
                                            .groupBy("domaine") \
                                            .count() \
                                            .orderBy(col("count").desc()),
        "top_authors_by_domain": lambda df: df.groupBy("domaine", "author") \
                                            .count() \
                                            .orderBy(col("domaine").asc(), col("count").desc()),
        "publication_trends": lambda df: df.withColumn("year", col("year")) \
                                        .groupBy("year") \
                                        .count() \
                                        .orderBy(col("year").asc()),
    }
    for core in cores:
        for query_name, query_func in queries.items():
            # Configurer Spark pour le nombre de cœurs
            spark.conf.set("spark.master", f"local[{core}]")

            # Mesurer le temps d'exécution
            start_time = time.time()
            query_func(df)  # Exécuter la requête
            execution_time = time.time() - start_time

            # Enregistrer les résultats
            results.append({
                "cores": core,
                "query": query_name,
                "time": execution_time,
            })

    spark.stop()

    # 4. Retourner les résultats sous forme de tableau
    return render(request, "myapp/benchmark.html", {"results": results})

def complex_query_view(request):
    # 1. Configuration de Spark
    spark = SparkSession.builder \
        .appName("Query View") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .master("local[*]") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()
    
    # 2. Charger les données depuis la base de données SQLite
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite",
        driver="org.sqlite.JDBC",
        dbtable="hal"
    ).load()

    # 3. Exécuter la requête complexe avec Spark
    results = df.groupBy("DOMAINE") \
        .count() \
        .orderBy(col("count").desc()) \
        .limit(30) \
        .toPandas()  # Convertir les résultats en Pandas DataFrame

    # Afficher requête
    print(results)

    # Vérification si les résultats sont vides
    if results.empty:
        return render(request, 'myapp/complex_query_graph.html', {'error': 'Aucune donnée disponible pour le graphique.'})

    # 4. Créer un graphique en barre avec Matplotlib
    plt.figure(figsize=(10, 6))  # Taille du graphique
    plt.bar(results['DOMAINE'], results['count'], color='skyblue')  # Création du graphique en barre
    plt.xlabel('Domaine')  # Label de l'axe X
    plt.ylabel('Nombre de Publications')  # Label de l'axe Y
    plt.title('Nombre de Publications par Domaine (>= 2022)')  # Titre du graphique
    plt.xticks(rotation=45, ha='right')  # Rotation des labels de l'axe X pour une meilleure lisibilité
    plt.tight_layout()  # Ajustement pour éviter que les labels ne se chevauchent

    # 5. Sauvegarder le graphique en mémoire et l'encoder en base64
    buffer = io.BytesIO()  # Créer un buffer pour stocker l'image
    plt.savefig(buffer, format='png')  # Sauvegarder l'image au format PNG
    buffer.seek(0)  # Revenir au début du buffer
    image_png = buffer.getvalue()  # Obtenir l'image en tant que données binaires
    buffer.close()  # Fermer le buffer

    # Encoder l'image en base64 pour l'envoyer à l'HTML
    graph = base64.b64encode(image_png).decode('utf-8')

    # 6. Retourner la page HTML avec le graphique encodé en base64
    return render(request, 'myapp/complex_query_graph.html', {'graph': graph})


# def query_db_view(request):
#     query = request.GET.get("query", "")
#     if not query:
#         return JsonResponse({"error": "No query provided"}, status=400)

#     try:
#         # Execute the PySpark AI query
#         result_df = query_sqlite(query)

#         # Collect result into a list of dictionaries
#         results = result_df.toPandas().to_dict(orient="records")

#         return JsonResponse({"results": results}, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

def benchmark_articles_view(request):
    # 1. Configuration PySpark
    spark = SparkSession.builder \
        .appName("Benchmark Articles") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .master("local[*]") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()

    # 2. Load the new database (articles table)
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/articles.sqlite",  # Update with the correct path
        driver="org.sqlite.JDBC",
        dbtable="articles"
    ).load()

    # 3. Define Benchmark Queries
    results = []
    cores = [1, 2, 4]  # Number of cores
    repetitions = 100  # Number of repetitions for averaging
    queries = {
        "total_articles": lambda df: df.count(),  # Count total articles
        "articles_per_year": lambda df: df.withColumn("year", year(col("publication_date"))) \
                                          .groupBy("year") \
                                          .count() \
                                          .orderBy(col("year").asc()) \
                                          .collect(),
        "most_common_types": lambda df: df.groupBy("type") \
                                          .count() \
                                          .orderBy(col("count").desc()) \
                                          .collect(),
        "top_contributors": lambda df: df.groupBy("contributors") \
                                         .count() \
                                         .orderBy(col("count").desc()) \
                                         .limit(10) \
                                         .collect(),
        "articles_in_time_range": lambda df: df.filter((year(col("publication_date")) >= 2015) & 
                                                        (year(col("publication_date")) <= 2020)) \
                                               .count(),
        "average_articles_per_topic": lambda df: df.groupBy("topic") \
                                                   .count() \
                                                   .agg({"count": "avg"}) \
                                                   .collect(),
    }

    # 4. Execute Queries and Measure Execution Time
    for core in cores:
        for query_name, query_func in queries.items():
            spark.conf.set("spark.master", f"local[{core}]")

            total_time = 0
            for _ in range(repetitions):
                spark.catalog.clearCache()  # Clear cache to remove optimization effects

                start_time = time.time()
                query_func(df)  # Execute query
                execution_time = time.time() - start_time

                total_time += execution_time

            # Calculate average execution time
            average_time = total_time / repetitions

            # Store results
            results.append({
                "cores": core,
                "query": query_name,
                "average_time": average_time,
            })

    spark.stop()

    # 5. Return Results to HTML Template
    return render(request, "myapp/benchmark_articles.html", {"results": results})


def complex_query_view_articles(request):
    # 1. Configure PySpark
    spark = SparkSession.builder \
        .appName("Query View - Articles") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .master("local[*]") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()

    # 2. Load Data from the Articles Database
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/articles.sqlite",  # Update the path
        driver="org.sqlite.JDBC",
        dbtable="articles"
    ).load()

    # 3. Execute a Complex Query with Spark
    results = df.withColumn("year", year(col("publication_date"))) \
                .groupBy("year") \
                .count() \
                .orderBy(col("year").asc()) \
                .toPandas()  # Convert results to Pandas DataFrame

    # Print results for debugging
    print(results)

    # 4. Check if the results are empty
    if results.empty:
        return render(request, 'myapp/complex_query_graph_articles.html', {'error': 'No data available for the graph.'})

    # 5. Create a Bar Chart with Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(results['year'], results['count'], color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Number of Articles')
    plt.title('Number of Articles Published Per Year')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # 6. Save the Graph in Memory and Encode in Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')

    # 7. Render the Template with the Graph
    return render(request, 'myapp/complex_query_graph_articles.html', {'graph': graph})

# Initialize Spark Session
def get_spark_session():
    return SparkSession.builder \
        .appName("AI Search") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .master("local[*]") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()


def ai_search_view(request):
    # 1. Start PySpark
    spark = get_spark_session()

    # 2. Load Articles Database
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/articles.sqlite",
        driver="org.sqlite.JDBC",
        dbtable="articles"
    ).load()

    # 3. Get User Query
    query = request.GET.get('query', '')

    # 4. Filter the Data with AI Search
    if query:
        filtered_df = df.filter(col("title").like(f"%{query}%") | col("abstract").like(f"%{query}%"))
        results = filtered_df.toPandas()
    else:
        results = pd.DataFrame()  # Empty DataFrame if no query

    # 5. Generate Bar Chart for Topics
    if not results.empty:
        topic_counts = results['topic'].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(topic_counts.index, topic_counts.values, color='skyblue')
        plt.xlabel('Topic')
        plt.ylabel('Number of Articles')
        plt.title(f'Articles Related to "{query}" by Topic')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Save the Graph in Memory
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph = base64.b64encode(image_png).decode('utf-8')
    else:
        graph = None

    # 6. Render the Results in HTML
    return render(request, 'myapp/ai_search.html', {'graph': graph, 'query': query, 'results': results.to_dict(orient='records')})


# 7. CSV Export Function
def export_csv(request):
    query = request.GET.get('query', '')

    # Start PySpark
    spark = get_spark_session()

    # Load Articles Database
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite",
        driver="org.sqlite.JDBC",
        dbtable="hal"
    ).load()

    # Filter Data
    filtered_df = df.filter(col("title").like(f"%{query}%") | col("abstract").like(f"%{query}%"))
    results = filtered_df.toPandas()

    # Generate CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="search_results_{query}.csv"'
    results.to_csv(response, index=False)

    return response


# 8. Image Download (ZIP)
def download_images(request):
    query = request.GET.get('query', '')

    # Create ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Generate Images
        for i in range(5):  # Example: Create 5 images
            plt.figure(figsize=(6, 4))
            plt.text(0.5, 0.5, f"AI Generated Image {i+1}\nQuery: {query}", fontsize=12, ha='center')
            plt.axis("off")

            # Save Image to Memory
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)

            # Add Image to ZIP
            zip_file.writestr(f"image_{i+1}.png", img_buffer.getvalue())

    # Return ZIP File
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="images_{query}.zip"'
    return response


# Initialize PySpark
def get_spark_session():
    return SparkSession.builder \
        .appName("AI Search") \
        .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
        .master("local[*]") \
        .config("spark.executor.memory", "2g") \
        .getOrCreate()

# AI-Driven DataFrame Search
def ai_dataframe_search(request):
    spark = get_spark_session()

    # Load Articles Database
    df = spark.read.format("jdbc").options(
        url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite",
        driver="org.sqlite.JDBC",
        dbtable="hal"
    ).load()

    # Initialize PySpark AI
    spark_ai = SparkAI(spark_session=spark)
    
    # Get User Query
    query = request.GET.get('query', '')

    # Use PySpark AI to generate an SQL query and execute it
    if query:
        ai_generated_query = spark_ai.ask(f"Create a DataFrame for the query: {query}. Output should include relevant columns.")
        print(f"AI-Generated Query: {ai_generated_query}")

        # Run the AI-generated query
        results_df = spark_ai.sql(ai_generated_query)
        results = results_df.toPandas()
    else:
        results = pd.DataFrame()

    return render(request, 'myapp/ai_dataframe_search.html', {'query': query, 'results': results.to_dict(orient='records')})


import csv
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import connection

def search_sql(request):
    query = request.GET.get('query', '')
    page_number = request.GET.get('page', 1)

    # If query exists, execute it
    if query:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]  # Get column names

        # Use Django paginator for large result sets
        paginator = Paginator(rows, 10)  # Show 10 results per page
        page_obj = paginator.get_page(page_number)

        # Convert rows to a list of dictionaries
        results = [dict(zip(columns, row)) for row in page_obj.object_list]

        return render(request, 'myapp/sql_search.html', {'query': query, 'results': results, 'page_obj': page_obj})
    
    return render(request, 'myapp/sql_search.html', {'query': query})

def download_csv(request):
    query = request.GET.get('query', '')

    if not query:
        return HttpResponse("No query provided", status=400)

    # Execute SQL query
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # Get column names

    # Create HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="query_results.csv"'

    writer = csv.writer(response)
    writer.writerow(columns)  # Write column headers
    writer.writerows(rows)  # Write data rows

    return response

import time
from pyspark_ai import SparkAI

# Initialize Spark session and PySpark AI
spark = SparkSession.builder \
    .appName("Natural Language SQL Query") \
    .config("spark.jars", "/home/menth/bigdata/app/Analyse-des-publications-UPEC/sqlite-jdbc-3.48.0.0.jar") \
    .master("local[*]") \
    .getOrCreate()

spark_ai = SparkAI()
spark_ai.activate()  # Activating PySpark AI for DataFrame transformations

# View to handle the query
def transform_sql_query(request):
    if request.method == "GET":
        query = request.GET.get('query', '')  # Get query from the search bar

        # Check if the query exists
        if query:
            try:
                # Load the SQLite data
                df = spark.read.format("jdbc").options(
                    url="jdbc:sqlite:/home/menth/bigdata/app/Analyse-des-publications-UPEC/db.sqlite",
                    driver="org.sqlite.JDBC",
                    dbtable="hal"
                ).load()

                # Use PySpark AI to transform the query
                transformed_df = df.ai.transform(query)  # Run the natural language query transformation

                # Convert the results to Pandas for easier rendering
                transformed_results = transformed_df.toPandas()

                # Render the page with the transformed results
                return render(request, 'myapp/sql_query_results.html', {'results': transformed_results.to_html()})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return render(request, 'myapp/sql_query_results.html', {'error': 'Please enter a query'})
    return render(request, 'myapp/sql_query_results.html')

>>>>>>> Stashed changes
>>>>>>> Stashed changes
