from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("sobre/", views.sobre, name="sobre"),
    path("entrar/", views.EntrarView.as_view(), name="login"),
    path("sair/", views.SairView.as_view(), name="logout"),
    path("cadastro/", views.cadastrar, name="cadastro"),
    path("autores/", views.autores, name="autores"),
    path("categorias/", views.categorias, name="categorias"),
    path("livros/", views.livros, name="livros"),
    path("emprestimos/", views.emprestimos, name="emprestimos"),
    path("multas/", views.multas, name="multas"),
    path("adicionar/<str:tipo>/", views.adicionar, name="adicionar"),
    path("editar/<str:tipo>/<int:pk>/", views.editar, name="editar"),
    path("excluir/<str:tipo>/<int:pk>/", views.excluir, name="excluir"),
    path("emprestimos/<int:pk>/devolver/", views.devolver, name="devolver"),
    path("emprestimos/<int:pk>/multa/", views.gerar_multa, name="gerar_multa"),
    path("multas/<int:pk>/pagar/", views.pagar_multa, name="pagar_multa"),
    
]
