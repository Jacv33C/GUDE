from django.db import models

# Create your models here.

#Materias
class Curso(models.Model):
    codigo = models.CharField(primary_key=True,max_length=6)
    nombre = models.CharField(max_length=50)
    creditos = models.PositiveSmallIntegerField()

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre,self.creditos)
    
    #Docentes
    class Docente(models.Model):
         matricula = models.CharField(primary_key=True, max_length=9)
    
    #Alumnos
    class Alumno(models.Model):
        matricula = models.CharField(primary_key=True, max_length=9)
        nombre = models.CharField(max_length=100)
        correo = models.EmailField(unique=True)

        