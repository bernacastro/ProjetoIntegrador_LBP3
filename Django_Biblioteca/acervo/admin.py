from django.contrib import admin
from .models import Autor, Categoria, Livro, Emprestimo, Multa

admin.site.register([Autor, Categoria, Livro, Emprestimo, Multa])
