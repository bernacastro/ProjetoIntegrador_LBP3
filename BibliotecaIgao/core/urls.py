from django.urls import path
from .views import inicio, sobre, livros, autores, emprestimos, generos, multas

urlpatterns = [
    path('', inicio, name='inicio'),
    path('sobre/', sobre, name='sobre'),
    path('livros/', livros, name='livros'),
    path('autores/', autores, name='autores'),
    path('emprestimos/', emprestimos, name='emprestimos'),
    path('generos/', generos, name='generos'),
    path('multas/', multas, name='multas'),
]