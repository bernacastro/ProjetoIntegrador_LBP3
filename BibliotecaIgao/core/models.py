from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(blank=True, null=True)
    nacionalidade = models.CharField(max_length=50)

    def __str__(self): return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self): return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    data_publicacao = models.DateField(blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True, blank=True, related_name="livros")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="livros")
    quantidade_total = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    quantidade_disponivel = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk and self.quantidade_disponivel is None:
            self.quantidade_disponivel = self.quantidade_total
        super().save(*args, **kwargs)

    def __str__(self): return self.titulo


class Emprestimo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="emprestimos")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="emprestimos")
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateTimeField(blank=True, null=True)

    def __str__(self): return f"{self.livro} — {self.usuario}"


class Multa(models.Model):
    PENDENTE, PAGA = "PENDENTE", "PAGA"
    STATUS = [(PENDENTE, "Pendente"), (PAGA, "Paga")]
    emprestimo = models.OneToOneField(Emprestimo, on_delete=models.CASCADE, related_name="multa")
    valor = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    data_geracao = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDENTE)

    def __str__(self): return f"Multa #{self.pk} - {self.get_status_display()}"

class Usuario(AbstractUser):
    ALUNO, PROFESSOR = "ALUNO", "PROFESSOR"
    TIPOS = [(ALUNO, "Aluno"), (PROFESSOR, "Professor")]

    tipo = models.CharField(max_length=20, choices=TIPOS, default=ALUNO)
    
    def __str__(self):
        return self.username