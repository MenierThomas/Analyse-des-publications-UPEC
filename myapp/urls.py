# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('query-db/', views.query_db_view, name='query_db'),
]
