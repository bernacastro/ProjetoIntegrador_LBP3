from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    isbn = models.IntegerField(max_length=13)
    autor = models.ForeignKey('Autor', default="Desconhecido", on_delete=models.SET_DEFAULT)
    data_publicacao = models.DateField()
    quantidade = models.IntegerField(default=1)


    def __str__(self):
        return self.titulo
    
class Autor(models.Model):
    nome = models.CharField(150)
    data_nascimento = models.DateField()
    nacionalidade = models.CharField()