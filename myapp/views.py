# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .pyspark_ai import query_sqlite  # Import from pyspark_ai.py


def main_page(request):
    return render(request, 'myapp/main_page.html')


def query_db_view(request):
    query = request.GET.get("query", "")
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    try:
        # Execute the PySpark AI query
        result_df = query_sqlite(query)

        # Collect result into a list of dictionaries
        results = result_df.toPandas().to_dict(orient="records")

        return JsonResponse({"results": results}, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
