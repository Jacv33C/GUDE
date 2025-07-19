from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('registrarMateria/', views.registrarMateria),
     path('materias/', views.materias, name='materias'),
]
