from django.urls import path
from . import views


urlpatterns = [
    # Página de login (redirige a home o baseAlumnos)
    path('', views.login_view, name='login'),

    # Página principal (usuario personal)
    path('home/', views.home, name='home'),

    # Página para alumnos después del login
    path('baseAlumnos/', views.baseAlumnos, name='baseAlumnos'),

    # Sección de materias
    path('materias/', views.materias, name='materias'),
    path('materias/registrarMateria/', views.registrarMateria, name='registrarMateria'),
    path('materias/eliminacionCurso/<str:codigo>/', views.eliminacionCurso, name='eliminacionCurso'),
    path('materias/edicionCurso/<str:codigo>/', views.edicionCurso, name='edicionCurso'),
    path('materias/editarMateria/', views.editarMateria, name='editarMateria'),
    path('homebasealumnos/', views.homebasealumnos, name='homebasealumnos'),
    path('cargamaterias/', views.cargamateria, name= 'cargamaterias'),
    path('nuevoalumno/', views.nuevoalumno, name= 'nuevoalumno'),
]