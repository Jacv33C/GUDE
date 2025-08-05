from django.db import models
from django.utils import timezone

# Materias
class Curso(models.Model):
    codigo = models.CharField(primary_key=True, max_length=6)
    nombre = models.CharField(max_length=50)
    creditos = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.creditos})"


# Docentes
class Docente(models.Model):
    id = models.CharField(primary_key=True, max_length=9)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    rfc = models.CharField(max_length=13)
    password = models.CharField(max_length=50, default='123456')
    cursos = models.ManyToManyField('Curso', related_name='docentes')

    def __str__(self):
        return self.nombre


# Alumnos
class Alumno(models.Model):
    matricula = models.CharField(primary_key=True, max_length=9)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    curp = models.CharField(max_length=18, unique=True)

    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('sabatico', 'Sabático'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    cursos = models.ManyToManyField('Curso', related_name='alumnos', blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.matricula}"



from django.db import models

class Tarea(models.Model):
    curso = models.ForeignKey(Curso, related_name='tareas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_entrega = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.titulo} - {self.curso.nombre}"
