from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError
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

def eh_admin(user):
    return user.is_staff or user.is_superuser

# --- AUTENTICAÇÃO E PÁGINAS INICIAIS ---

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


# --- LISTAGENS ---

@login_required
def autores(request):
    return render(request, "core/lista_autores.html", {"autores": Autor.objects.all().order_by("nome")})


@login_required
def categorias(request):
    return render(request, "core/lista_generos.html", {"categorias": Categoria.objects.all().order_by("nome")})


@login_required
def livros(request):
    return render(
        request,
        "core/lista_livros.html",
        {"livros": Livro.objects.select_related("autor", "categoria").all().order_by("titulo")},
    )


@login_required
def emprestimos(request):
    return render(
        request,
        "core/lista_emprestimos.html",
        {"emprestimos": Emprestimo.objects.select_related("livro", "usuario").all().order_by("-data_emprestimo")},
    )


@login_required
def multas(request):
    return render(
        request,
        "core/lista_multas.html",
        {"multas": Multa.objects.select_related("emprestimo").all().order_by("-data_geracao")},
    )


# --- CONFIGURAÇÃO E VIEWS DE EDIÇÃO / EXCLUSÃO ---

MODEL_CONFIG = {
    "autor": {"model": Autor, "form": AutorForm, "title": "Autor", "redirect": "autores"},
    "categoria": {"model": Categoria, "form": CategoriaForm, "title": "Categoria", "redirect": "categorias"},
    "livro": {"model": Livro, "form": LivroForm, "title": "Livro", "redirect": "livros"},
    "emprestimo": {"model": Emprestimo, "form": EmprestimoForm, "title": "Empréstimo", "redirect": "emprestimos"},
}


@login_required
def editar(request, tipo, pk):

    # Autor, categoria e livro só podem ser
    # criados ou editados pelo administrador.
    if tipo in ["autor", "categoria", "livro"] and not eh_admin(request.user):
        return redirect("inicio")

    # Usuário comum pode criar empréstimo,
    # mas não pode editar um empréstimo existente.
    if tipo == "emprestimo" and pk != 0 and not eh_admin(request.user):
        return redirect("emprestimos")

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

            # Só diminui a quantidade quando um empréstimo é criado.
            if tipo == "emprestimo" and instance is None:
                obj.livro.quantidade_disponivel -= 1
                obj.livro.save(update_fields=["quantidade_disponivel"])

            return redirect(success_name)
    else:
        form = form_class(instance=instance)

    return render(
        request,
        "core/forms.html",
        {
            "form": form,
            "titulo": f"{title} (editar)" if instance else f"{title} (novo)",
        },
    )

@login_required
def excluir(request, tipo, pk):
    config = MODEL_CONFIG.get(tipo)
    if not config:
        return redirect("inicio")

    obj = get_object_or_404(config["model"], pk=pk)

    if request.method == "POST":
        try:
            if tipo == "emprestimo" and obj.data_devolucao_real is None:
                obj.livro.quantidade_disponivel += 1
                obj.livro.save(update_fields=["quantidade_disponivel"])

            obj.delete()
            return redirect(config["redirect"])
            
        except ProtectedError:
            # Se o banco bloquear a exclusão, renderiza a tela de erro
            return render(
                request, 
                "core/exclusao_protegida.html", 
                {"tipo": config["title"], "objeto": obj}
            )

    return render(
        request,
        "core/confirmar_exclusao.html",
        {
            "objeto": obj,
            "tipo": config["title"],
            "url_cancelar": config["redirect"],
        },
    )

@login_required
def adicionar(request, tipo):
    # Apenas administradores podem adicionar autor, categoria e livro
    if tipo in ["autor", "categoria", "livro"] and not eh_admin(request.user):
        return redirect("inicio")

    MAPA_FORMULARIOS = {
        "autor": (AutorForm, "Autor", "autores"),
        "categoria": (CategoriaForm, "Categoria", "categorias"),
        "livro": (LivroForm, "Livro", "livros"),
        "emprestimo": (EmprestimoForm, "Empréstimo", "emprestimos"),
    }

    if tipo not in MAPA_FORMULARIOS:
        return redirect("inicio")

    form_class, title, success_name = MAPA_FORMULARIOS[tipo]

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save()

            if tipo == "emprestimo":
                obj.livro.quantidade_disponivel -= 1
                obj.livro.save(update_fields=["quantidade_disponivel"])

            return redirect(success_name)
    else:
        form = form_class()

    return render(
        request,
        "core/forms.html",
        {"form": form, "titulo": f"Novo {title}"},
    )

# --- AÇÕES ESPECÍFICAS ---

@login_required
def devolver(request, pk):
    if request.method != "POST":
        return redirect("emprestimos")

    emprestimo = get_object_or_404(Emprestimo, pk=pk)

    if emprestimo.data_devolucao_real is None:
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.save(update_fields=["data_devolucao_real"])

        emprestimo.livro.quantidade_disponivel += 1
        emprestimo.livro.save(update_fields=["quantidade_disponivel"])

    return redirect("emprestimos")


@login_required
def gerar_multa(request, pk):
    if request.method != "POST":
        return redirect("multas")

    emprestimo = get_object_or_404(Emprestimo, pk=pk)

    if not Multa.objects.filter(emprestimo=emprestimo).exists():

        if emprestimo.data_devolucao_real:
            data_referencia = emprestimo.data_devolucao_real.date()
        else:
            data_referencia = timezone.localdate()

        if data_referencia > emprestimo.data_devolucao_prevista:
            dias_atraso = (data_referencia - emprestimo.data_devolucao_prevista).days

            valor = Decimal(dias_atraso) * Decimal("2.00")

            Multa.objects.create(
                emprestimo=emprestimo,
                valor=valor,
            )

    return redirect("multas")


@login_required
def pagar_multa(request, pk):
    if request.method != "POST":
        return redirect("multas")

    multa = get_object_or_404(Multa, pk=pk)

    if multa.status == Multa.PENDENTE:
        multa.status = Multa.PAGA
        multa.save(update_fields=["status"])

    return redirect("multas")