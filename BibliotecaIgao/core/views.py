from django.http import HttpResponse
from django.shortcuts import render

def inicio(request):
    return render(request, 'core/inicio.html')

def sobre(request):
    return render(request, 'core/sobre.html')

def livros(request):
    return render(request, 'core/lista_livros.html')

def autores(request):
    return render(request, 'core/lista_autores.html')

def emprestimos(request):
    return render(request, 'core/lista_emprestimos.html')

def generos(request):
    return render(request, 'core/lista_generos.html')

def multas(request):
    return render(request, 'core/lista_multas.html')

def not_found(request, exception):
    return render(request, 'core/404.html', status=404)