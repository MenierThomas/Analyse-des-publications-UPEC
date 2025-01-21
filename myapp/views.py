# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
# from .pyspark_ai import query_sqlite  # Import from pyspark_ai.py
from .pyspark_code import run_pyspark_task


def main_page(request):
    return render(request, 'myapp/main_page.html')


def pyspark_view(request):
    # Run PySpark task and get results
    results = run_pyspark_task()

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
