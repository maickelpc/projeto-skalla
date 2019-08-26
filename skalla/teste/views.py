from django.shortcuts import render
# from django.template import Context, Template
from django.http import HttpResponse


# Create your views here.

def hello(request):
    return render(request, 'home.html', {'usuario': 'FULANO'})