from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import (
    AutorForm,
    CadastroForm,
    CategoriaForm,
    EmprestimoForm,
    LivroForm,
)
from .models import Autor, Categoria, Emprestimo, Livro, Multa


def inicio(request):
    return render(
        request,
        "core/inicio.html",
        {
            "livros": Livro.objects.count(),
            "emprestimos": Emprestimo.objects.filter(data_devolucao_real__isnull=True).count(),
            "multas": Multa.objects.filter(status=Multa.PENDENTE).count(),
        },
    )


def sobre(request):
    return render(request, "core/sobre.html")


class EntrarView(LoginView):
    template_name = "core/login.html"
    next_page = reverse_lazy("inicio")


class SairView(LogoutView):
    next_page = reverse_lazy("inicio")


def cadastrar(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("inicio")
    else:
        form = CadastroForm()

    return render(request, "core/cadastro.html", {"form": form, "titulo": "Cadastro"})


@login_required
def autores(request):
    return render(request, "core/lista_autores.html", {"autores": Autor.objects.all().order_by("nome")})


@login_required
def categorias(request):
    return render(request, "core/lista_generos.html", {"categorias": Categoria.objects.all().order_by("nome")})


@login_required
def livros(request):
    return render(request, "core/lista_livros.html", {"livros": Livro.objects.select_related("autor", "categoria").all().order_by("titulo")})


@login_required
def emprestimos(request):
    return render(
        request,
        "core/lista_emprestimos.html",
        {"emprestimos": Emprestimo.objects.select_related("livro", "usuario").all().order_by("-data_emprestimo")},
    )


@login_required
def multas(request):
    return render(request, "core/lista_multas.html", {"multas": Multa.objects.select_related("emprestimo").all().order_by("-data_geracao")})


@login_required
def editar(request, tipo, pk):
    form_class = None
    model = None
    title = ""
    success_name = None

    if tipo == "autor":
        model = Autor
        form_class = AutorForm
        title = "Autor"
        success_name = "autores"
    elif tipo == "categoria":
        model = Categoria
        form_class = CategoriaForm
        title = "Categoria"
        success_name = "categorias"
    elif tipo == "livro":
        model = Livro
        form_class = LivroForm
        title = "Livro"
        success_name = "livros"
    elif tipo == "emprestimo":
        model = Emprestimo
        form_class = EmprestimoForm
        title = "Empréstimo"
        success_name = "emprestimos"
    else:
        return redirect("inicio")

    instance = None if pk == 0 else get_object_or_404(model, pk=pk)

    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            if tipo == "emprestimo" and not obj.data_devolucao_real:
                obj.livro.quantidade_disponivel = max(0, obj.livro.quantidade_disponivel - 1)
                obj.livro.save(update_fields=["quantidade_disponivel"])
            return redirect(success_name)
    else:
        form = form_class(instance=instance)

    return render(request, "core/forms.html", {"form": form, "titulo": f"{title} (editar)" if instance else f"{title} (novo)"})


@login_required
def excluir(request, tipo, pk):
    if tipo == "autor":
        obj = get_object_or_404(Autor, pk=pk)
    elif tipo == "categoria":
        obj = get_object_or_404(Categoria, pk=pk)
    elif tipo == "livro":
        obj = get_object_or_404(Livro, pk=pk)
    elif tipo == "emprestimo":
        obj = get_object_or_404(Emprestimo, pk=pk)
        if obj.data_devolucao_real is None:
            obj.livro.quantidade_disponivel += 1
            obj.livro.save(update_fields=["quantidade_disponivel"])
    else:
        return redirect("inicio")

    obj.delete()
    return redirect({"autor": "autores", "categoria": "categorias", "livro": "livros", "emprestimo": "emprestimos"}[tipo])


@login_required
def devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.data_devolucao_real is None:
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.save(update_fields=["data_devolucao_real"])
        emprestimo.livro.quantidade_disponivel += 1
        emprestimo.livro.save(update_fields=["quantidade_disponivel"])
    return redirect("emprestimos")


@login_required
def gerar_multa(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if not Multa.objects.filter(emprestimo=emprestimo).exists():
        if emprestimo.data_devolucao_real is None and emprestimo.data_devolucao_prevista < timezone.localdate():
            dias_atraso = (timezone.localdate() - emprestimo.data_devolucao_prevista).days
            valor = Decimal(dias_atraso) * Decimal("2.00")
            Multa.objects.create(emprestimo=emprestimo, valor=valor)
    return redirect("multas")


@login_required
def pagar_multa(request, pk):
    multa = get_object_or_404(Multa, pk=pk)
    multa.status = Multa.PAGA
    multa.save(update_fields=["status"])
    return redirect("multas")
