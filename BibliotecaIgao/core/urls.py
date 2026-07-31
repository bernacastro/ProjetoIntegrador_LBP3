from django.urls import path
from .views import inicio, sobre

urlpatterns = [
    path('', inicio, name='inicio'),
    path('sobre/', sobre, name='sobre'),
    
]