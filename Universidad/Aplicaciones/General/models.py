from django.db import models

# Materias
class Curso(models.Model):
    codigo = models.CharField(primary_key=True, max_length=6)
    nombre = models.CharField(max_length=50)
    creditos = models.PositiveSmallIntegerField()

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre, self.creditos)

from django.db import models

# Docentes
class Docente(models.Model):
    id = models.CharField(primary_key=True, max_length=9)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    rfc = models.CharField(max_length=13, unique=True)
    password = models.CharField(max_length=6, null=True, blank=True)


    def __str__(self):
        return f"{self.nombre} ({self.id})"

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

    def __str__(self):
        return f"{self.nombre} - {self.matricula}"
