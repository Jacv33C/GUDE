from django.shortcuts import render, redirect
from .models import Curso

def home(request):
    return render(request, "Home.html") 

def registrarMateria(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    creditos = request.POST['numCreditos']

    Curso.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
    return redirect('materias')  # usa el nombre de la URL para redirigir

def eliminacionCurso(request, codigo):
    curso = Curso.objects.get(codigo=codigo)
    curso.delete()
    return redirect('materias')  # corregido aquí para redirigir correctamente

def materias(request):
    cursos = Curso.objects.all()
    return render(request, "Materias.html", {"cursos": cursos})
