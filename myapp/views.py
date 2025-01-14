# myapp/views.py
from django.shortcuts import render

def main_page(request):
    return render(request, 'myapp/main_page.html')
