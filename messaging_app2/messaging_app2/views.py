# messaging_app2/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
