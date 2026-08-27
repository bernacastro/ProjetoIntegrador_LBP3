from django.contrib import admin

from .models import Autor, Categoria, Emprestimo, Livro, Multa, Usuario


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nome", "nacionalidade", "data_nascimento")
    search_fields = ("nome", "nacionalidade")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "isbn",
        "autor",
        "categoria",
        "quantidade_total",
        "quantidade_disponivel",
    )
    search_fields = ("titulo", "isbn", "autor__nome")
    list_filter = ("categoria", "autor")


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = (
        "livro",
        "usuario",
        "data_emprestimo",
        "data_devolucao_prevista",
        "data_devolucao_real",
    )
    search_fields = ("livro__titulo", "usuario__username")
    list_filter = ("data_devolucao_real",)


@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display = (
        "emprestimo",
        "valor",
        "data_geracao",
        "status",
    )
    list_filter = ("status",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "tipo", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("tipo", "is_staff", "is_active")