from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Todas las rutas relacionadas con materias con prefijo 'materias/'
    path('materias/', views.materias, name='materias'),
    path('materias/registrarMateria/', views.registrarMateria, name='registrarMateria'),
    path('materias/eliminacionCurso/<str:codigo>/', views.eliminacionCurso, name='eliminacionCurso'),
    path('materias/edicionCurso/<str:codigo>/', views.edicionCurso, name='edicionCurso'),
    path('materias/editarMateria/', views.editarMateria, name='editarMateria'),

]
