# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('pyspark/', views.pyspark_view, name='pyspark_view'),
    # path('query-db/', views.query_db_view, name='query_db'),
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
=======
    path("benchmark/", views.benchmark_view, name="benchmark"),
    path('complex-query-graph/', views.complex_query_view, name='complex_query_graph'),
    path('benchmark_articles/', views.benchmark_articles_view, name='benchmark_articles'),
    path('complex-query-graph-articles/', views.complex_query_view_articles, name='complex_query_graph_articles'),
    path('ai-search/', views.ai_search_view, name='ai_search'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('download-images/', views.download_images, name='download_images'),
    path('ai-dataframe-search/', views.ai_dataframe_search, name='ai_dataframe_search'),
    path('search-sql/', views.search_sql, name='search_sql'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('transform_sql_query/', views.transform_sql_query, name='transform_sql_query'),
>>>>>>> Stashed changes
>>>>>>> Stashed changes
]

