from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), 
    path('home/', views.home, name='home'),
    path('materias/', views.materias, name='materias'),
    path('materias/registrarMateria/', views.registrarMateria, name='registrarMateria'),
    path('materias/eliminacionCurso/<str:codigo>/', views.eliminacionCurso, name='eliminacionCurso'),
    path('materias/edicionCurso/<str:codigo>/', views.edicionCurso, name='edicionCurso'),
    path('materias/editarMateria/', views.editarMateria, name='editarMateria'),
]
