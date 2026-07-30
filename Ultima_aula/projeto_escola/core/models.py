from django.db import models


class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    editora = models.CharField(max_length=100)
    ano_publicacao = models.IntegerField()
    quantidade = models.IntegerField(default=1)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    idade = models.IntegerField()
    curso = models.CharField(max_length=120)
    matricula = models.CharField(max_length=20, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
