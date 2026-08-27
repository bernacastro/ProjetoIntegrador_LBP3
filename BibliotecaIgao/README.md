# Biblioteca em Django

Versão independente do projeto Flask, desenvolvida com Django, SQLite, ORM, `ModelForm`, autenticação e CRUD protegido por login.

## Como executar

```powershell
cd Django_Biblioteca
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. O painel `/admin/` permite administrar todos os modelos.

## Regras implementadas

- Livros não podem ser emprestados quando não há exemplares disponíveis.
- Registrar/deletar/devolver empréstimos atualiza a quantidade disponível.
- Multas são calculadas em R$ 2,00 por dia de atraso e só pode haver uma por empréstimo.