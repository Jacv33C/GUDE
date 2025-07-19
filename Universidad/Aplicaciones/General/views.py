from django.shortcuts import render, redirect
from .models import Curso

# Create your views here.

def home(request):
    
    return render(request, "Home.html" ) 

def registrarMateria(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    creditos = request.POST['numCreditos']

    curso =     Curso.objects.create(codigo = codigo, nombre = nombre, creditos = creditos)
    return redirect('/materias')

def materias(request):
    cursos =  Curso.objects.all()
    return render(request, "Materias.html",{"cursos": cursos})