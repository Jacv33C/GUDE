from django.contrib import admin
from .models import Curso, Docente, Alumno
from .models import HistorialAcademico

admin.site.register(Curso)
admin.site.register(Docente)
admin.site.register(Alumno)
admin.site.register(HistorialAcademico) 