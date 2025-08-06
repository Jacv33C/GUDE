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
     path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

    # CRUD MATERIAS
    path('materias/', views.materias, name='materias'),
    path('materias/registrarMateria/', views.registrarMateria, name='registrarMateria'),
    path('materias/eliminacionCurso/<str:codigo>/', views.eliminacionCurso, name='eliminacionCurso'),
    path('materias/edicionCurso/<str:codigo>/', views.edicionCurso, name='edicionCurso'),
    path('materias/editarMateria/', views.editarMateria, name='editarMateria'),
 path('asignarMaterias/<str:docente_id>/', views.asignarMaterias, name='asignarMaterias'),
 path('ruta-guardardocente/', views.guardardocente, name='guardardocente'),
 





    # CRUD ALUMNOS
    path('nuevoalumno/', views.nuevoalumno, name='nuevoalumno'),
    path('alumnos/registrarAlumno/', views.registrarAlumno, name='registrarAlumno'),
    path('alumnos/edicionAlumno/<str:matricula>/', views.edicionAlumno, name='edicionAlumno'),
    path('alumnos/editarAlumno/', views.editarAlumno, name='editarAlumno'),
    path('alumnos/eliminacionAlumno/<str:matricula>/', views.eliminacionAlumno, name='eliminacionAlumno'),
    path('datosgeneralesalumnos', views.datosgeneralesalumnos, name="datosgeneralesalumnos"),
    path('alumno/cargar-materias/', views.cargar_materias_alumno, name='cargar_materias_alumno'),
    path('alumno/inscribir-materias/', views.inscribirMateriasAlumno, name='inscribirMateriasAlumno'),

    # CRUD DOCENTES
    path('nuevodocente/', views.nuevodocente, name='nuevodocente'),
    path('docentes/registrarDocente/', views.registrarDocente, name='registrarDocente'),
    path('docentes/edicionDocente/<str:id>/', views.edicionDocente, name='edicionDocente'),
    path('buscar-materias/', views.buscar_materias, name='buscar_materias'),
    path('docentes/editarDocente/<str:id>/', views.editarDocente, name="editarDocente"),
    path('docentes/eliminacionDocente/<str:id>/', views.eliminacionDocente, name='eliminacionDocente'),
    path('baseDocentes/', views.baseDocentes, name="baseDocentes"),
    path('homebasedocentes/', views.homebasedocentes, name = "homebasedocentes"),
    path('datosgeneralesdocentes/', views.datosgeneralesdocentes, name = 'datosgeneralesdocentes'),
    path('docente/<str:id>/', views.detalle_docente, name='detalle_docente'),
   path('docente/<str:docente_id>/desasignar/<str:codigo>/', views.desasignar_materia, name='desasignar_materia'),
    path('verMateriasDocente/<str:docente_id>/', views.verMateriasDocente, name='verMateriasDocente'),
    path('materias-tareas/', views.listarMateriasConTareas, name='listarMateriasConTareas'),
    path('asignarMaterias/<int:docente_id>/', views.asignarMaterias, name='asignarMaterias'),
    path('tareas/<str:curso_codigo>/', views.agregarTarea, name='agregarTarea'),
    path('editar-tarea/<int:id>/', views.editar_tarea, name='editarTarea'),
path('eliminar-tarea/<int:id>/', views.eliminar_tarea, name='eliminarTarea'),
path('tareas/editar/<int:id>/', views.editar_tarea, name='editarTarea'),
path('alumno/<str:matricula>/tareas/', views.ver_tareas_alumno, name='TareasAlumnos'),











]
