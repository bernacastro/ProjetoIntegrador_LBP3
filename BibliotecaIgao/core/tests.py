from django.test import TestCase
from django.urls import reverse


class BibliotecaViewsTest(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("inicio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Painel")

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrar")
