from django.urls import path
from .views import (
    inicio,
    sobre,
    curso,
    lista_livros,
    detalhe_livro,
    lista_alunos,
    detalhe_aluno,
)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('sobre/', sobre, name='sobre'),
    path('curso/', curso, name='curso'),
    path('livros/', lista_livros, name='lista_livros'),
    path('livros/<int:id>/', detalhe_livro, name='detalhe_livro'),
    path('alunos/', lista_alunos, name='lista_alunos'),
    path('alunos/<int:id>/', detalhe_aluno, name='detalhe_aluno'),
]
