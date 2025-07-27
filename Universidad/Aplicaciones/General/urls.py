from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path('', views.login_view, name='login'),

    # VISTAS PRINCIPALES
    path('home/', views.home, name='home'),
    path('baseAlumnos/', views.baseAlumnos, name='baseAlumnos'),
    path('homebasealumnos/', views.homebasealumnos, name='homebasealumnos'),
    path('cargamaterias/', views.cargamateria, name='cargamaterias'),

    # CRUD MATERIAS
    path('materias/', views.materias, name='materias'),
    path('materias/registrarMateria/', views.registrarMateria, name='registrarMateria'),
    path('materias/eliminacionCurso/<str:codigo>/', views.eliminacionCurso, name='eliminacionCurso'),
    path('materias/edicionCurso/<str:codigo>/', views.edicionCurso, name='edicionCurso'),
    path('materias/editarMateria/', views.editarMateria, name='editarMateria'),

    # CRUD ALUMNOS
    path('nuevoalumno/', views.nuevoalumno, name='nuevoalumno'),
    path('alumnos/registrarAlumno/', views.registrarAlumno, name='registrarAlumno'),
    path('alumnos/edicionAlumno/<str:matricula>/', views.edicionAlumno, name='edicionAlumno'),
    path('alumnos/editarAlumno/', views.editarAlumno, name='editarAlumno'),
    path('alumnos/eliminacionAlumno/<str:matricula>/', views.eliminacionAlumno, name='eliminacionAlumno'),

    # CRUD DOCENTES
    path('nuevodocente/', views.nuevodocente, name='nuevodocente'),
    path('docentes/registrarDocente/', views.registrarDocente, name='registrarDocente'),
    path('docentes/edicionDocente/<str:id>/', views.edicionDocente, name='edicionDocente'),
    path('docentes/editarDocente/<str:id>/', views.editarDocente, name="editarDocente"),
    path('docentes/eliminacionDocente/<str:id>/', views.eliminacionDocente, name='eliminacionDocente'),
]
