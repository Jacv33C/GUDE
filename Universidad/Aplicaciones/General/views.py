from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso

def home(request):
    return render(request, "Home.html") 

def registrarMateria(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    creditos = request.POST['numCreditos']

    Curso.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
    return redirect('materias')  

def edicionCurso(request, codigo):
    curso = Curso.objects.get(codigo=codigo)
    cursos = Curso.objects.all()
    return render(request, "edicionCurso.html", {
        "curso": curso,  
        "cursos": cursos
    })

def eliminacionCurso(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    curso.delete()
    return redirect('materias')

def editarMateria(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    creditos = request.POST['numCreditos']

    curso = Curso.objects.get(codigo=codigo)
    curso.nombre = nombre
    curso.creditos = creditos
    curso.save()

    return redirect('materias')

def materias(request):
    cursos = Curso.objects.all()
    return render(request, "Materias.html", {"cursos": cursos})
