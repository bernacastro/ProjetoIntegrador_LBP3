from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import AutorForm, CadastroForm, CategoriaForm, EmprestimoForm, LivroForm
from .models import Autor, Categoria, Emprestimo, Livro, Multa


class EntrarView(LoginView):
    template_name = "acervo/login.html"


class SairView(LogoutView):
    pass


def cadastrar(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Conta criada com sucesso.")
            return redirect("inicio")
    else:
        form = CadastroForm()
    return render(request, "acervo/form.html", {"form": form, "titulo": "Criar conta"})


@login_required
def inicio(request):
    return render(request, "acervo/inicio.html", {"livros": Livro.objects.count(), "emprestimos": Emprestimo.objects.filter(data_devolucao_real__isnull=True).count(), "multas": Multa.objects.filter(status=Multa.PENDENTE).count()})


def crud(request, modelo, form_class, pagina, mensagem):
    objeto = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{mensagem} cadastrado(a) com sucesso.")
            return redirect(pagina)
    else: form = form_class()
    return render(request, "acervo/lista.html", {"form": form, "objetos": modelo.objects.all(), "titulo": mensagem, "pagina": pagina})


@login_required
def autores(request): return crud(request, Autor, AutorForm, "autores", "Autores")
@login_required
def categorias(request): return crud(request, Categoria, CategoriaForm, "categorias", "Categorias")


@login_required
def livros(request):
    consulta = request.GET.get("q", "")
    objetos = Livro.objects.select_related("autor", "categoria").filter(Q(titulo__icontains=consulta) | Q(isbn__icontains=consulta))
    if request.method == "POST":
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save(); messages.success(request, "Livro cadastrado com sucesso."); return redirect("livros")
    else: form = LivroForm()
    return render(request, "acervo/lista.html", {"form": form, "objetos": objetos, "titulo": "Livros", "pagina": "livros", "consulta": consulta})


@login_required
def editar(request, tipo, pk):
    configuracao = {"autor": (Autor, AutorForm, "autores", "Autores"), "categoria": (Categoria, CategoriaForm, "categorias", "Categorias"), "livro": (Livro, LivroForm, "livros", "Livros")}
    modelo, form_class, pagina, titulo = configuracao[tipo]
    objeto = get_object_or_404(modelo, pk=pk)
    form = form_class(request.POST or None, instance=objeto)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Alterações salvas."); return redirect(pagina)
    return render(request, "acervo/form.html", {"form": form, "titulo": f"Editar {titulo[:-1]}"})


@login_required
def excluir(request, tipo, pk):
    modelos = {"autor": (Autor, "autores"), "categoria": (Categoria, "categorias"), "livro": (Livro, "livros"), "emprestimo": (Emprestimo, "emprestimos"), "multa": (Multa, "multas")}
    modelo, pagina = modelos[tipo]; objeto = get_object_or_404(modelo, pk=pk)
    if request.method == "POST":
        if tipo == "emprestimo" and objeto.data_devolucao_real is None:
            livro = objeto.livro; livro.quantidade_disponivel += 1; livro.save(update_fields=["quantidade_disponivel"])
        objeto.delete(); messages.success(request, "Registro excluído."); return redirect(pagina)
    return render(request, "acervo/confirmar_exclusao.html", {"objeto": objeto})


@login_required
def emprestimos(request):
    if request.method == "POST":
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(); livro = emprestimo.livro
            livro.quantidade_disponivel -= 1; livro.save(update_fields=["quantidade_disponivel"])
            messages.success(request, "Empréstimo registrado."); return redirect("emprestimos")
    else: form = EmprestimoForm()
    return render(request, "acervo/emprestimos.html", {"form": form, "emprestimos": Emprestimo.objects.select_related("livro", "usuario").all()})


@login_required
def devolver(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.data_devolucao_real is None:
        emprestimo.data_devolucao_real = timezone.now(); emprestimo.save(update_fields=["data_devolucao_real"])
        livro = emprestimo.livro; livro.quantidade_disponivel += 1; livro.save(update_fields=["quantidade_disponivel"])
        messages.success(request, "Devolução registrada.")
    return redirect("emprestimos")


@login_required
def gerar_multa(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    referencia = emprestimo.data_devolucao_real.date() if emprestimo.data_devolucao_real else timezone.localdate()
    dias = max(0, (referencia - emprestimo.data_devolucao_prevista).days)
    if dias == 0: messages.info(request, "Este empréstimo não está atrasado.")
    else:
        multa, criada = Multa.objects.get_or_create(emprestimo=emprestimo, defaults={"valor": Decimal(dias) * Decimal("2.00")})
        messages.success(request, "Multa gerada." if criada else "Já existe multa para este empréstimo.")
    return redirect("emprestimos")


@login_required
def multas(request):
    return render(request, "acervo/multas.html", {"multas": Multa.objects.select_related("emprestimo__usuario", "emprestimo__livro")})


@login_required
def pagar_multa(request, pk):
    multa = get_object_or_404(Multa, pk=pk); multa.status = Multa.PAGA; multa.save(update_fields=["status"])
    messages.success(request, "Multa marcada como paga."); return redirect("multas")
