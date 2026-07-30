from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    return render(request, 'core/inicio.html')

def sobre(request):
    return render(request, 'core/sobre.html')