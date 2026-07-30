from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Autor, Categoria, Livro, Emprestimo


class BibliotecaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("ana", password="senha-segura")
        self.autor = Autor.objects.create(nome="Machado de Assis", nacionalidade="Brasileira")
        self.categoria = Categoria.objects.create(nome="Romance")
        self.livro = Livro.objects.create(titulo="Dom Casmurro", isbn="1234567890123", autor=self.autor, categoria=self.categoria, quantidade_total=1)
        self.client.force_login(self.user)

    def test_emprestimo_reduz_e_devolucao_recompoe_estoque(self):
        resposta = self.client.post(reverse("emprestimos"), {"usuario": self.user.pk, "livro": self.livro.pk, "data_devolucao_prevista": timezone.localdate() + timedelta(days=7)})
        self.assertRedirects(resposta, reverse("emprestimos"))
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.quantidade_disponivel, 0)
        emprestimo = Emprestimo.objects.get()
        self.client.get(reverse("devolver", args=[emprestimo.pk]))
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.quantidade_disponivel, 1)

    def test_paginas_do_crud_renderizam(self):
        for nome in ("inicio", "autores", "categorias", "livros", "emprestimos", "multas"):
            self.assertEqual(self.client.get(reverse(nome)).status_code, 200)
