from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Autor, Categoria, Livro, Emprestimo


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = "__all__"
        widgets = {"data_nascimento": forms.DateInput(attrs={"type": "date"})}


class CategoriaForm(forms.ModelForm):
    class Meta: model, fields = Categoria, ["nome"]


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ["titulo", "isbn", "data_publicacao", "autor", "categoria", "quantidade_total"]
        widgets = {"data_publicacao": forms.DateInput(attrs={"type": "date"})}


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["usuario", "livro", "data_devolucao_prevista"]
        widgets = {"data_devolucao_prevista": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        dados = super().clean()
        livro = dados.get("livro")
        if livro and livro.quantidade_disponivel < 1:
            self.add_error("livro", "Não há exemplares disponíveis para empréstimo.")
        if dados.get("data_devolucao_prevista") and dados["data_devolucao_prevista"] < timezone.localdate():
            self.add_error("data_devolucao_prevista", "A devolução prevista não pode ser no passado.")
        return dados


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
