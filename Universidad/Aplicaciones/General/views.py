from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Alumno

# LOGIN
def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "jacvpa33personal@gmail.com" and password == "001122":
            return redirect('home')
        elif username == "jacvpa33@gmail.com" and password == "001122":
            return redirect('baseAlumnos')
        else:
            error = "Usuario o contraseña incorrectos."

    return render(request, "login.html", {"error": error})


# VISTAS BÁSICAS
def home(request):
    return render(request, "home.html")

def baseAlumnos(request):
    return render(request, "BaseAlumnos.html")

def homebasealumnos(request):
    return render(request, "homebasealumnos.html")

def cargamateria(request):
    return render(request, "cargamateria.html")


# MATERIAS
def materias(request):
    cursos = Curso.objects.all()
    return render(request, "Materias.html", {"cursos": cursos})

def registrarMateria(request):
    if request.method == "POST":
        codigo = request.POST['txtCodigo']
        nombre = request.POST['txtNombre']
        creditos = request.POST['numCreditos']

        Curso.objects.create(codigo=codigo, nombre=nombre, creditos=creditos)
    return redirect('materias')

def edicionCurso(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    cursos = Curso.objects.all()
    return render(request, "edicionCurso.html", {
        "curso": curso,
        "cursos": cursos
    })

def editarMateria(request):
    if request.method == "POST":
        codigo = request.POST['txtCodigo']
        nombre = request.POST['txtNombre']
        creditos = request.POST['numCreditos']

        curso = Curso.objects.get(codigo=codigo)
        curso.nombre = nombre
        curso.creditos = creditos
        curso.save()
    return redirect('materias')

def eliminacionCurso(request, codigo):
    curso = get_object_or_404(Curso, codigo=codigo)
    curso.delete()
    return redirect('materias')


# ALUMNOS
def nuevoalumno(request):
    alumnos = Alumno.objects.all()
    return render(request, "nuevoalumno.html", {"alumnos": alumnos})

def registrarAlumno(request):
    if request.method == "POST":
        matricula = request.POST['txtMatricula']
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        curp = request.POST['txtCurp']
        estado = request.POST['selectEstado']

        Alumno.objects.create(
            matricula=matricula,
            nombre=nombre,
            correo=correo,
            curp=curp,
            estado=estado
        )
    return redirect('nuevoalumno')

def edicionAlumno(request, matricula):
    alumno = get_object_or_404(Alumno, matricula=matricula)
    alumnos = Alumno.objects.all()
    return render(request, "edicionAlumno.html", {"alumno": alumno, "alumnos": alumnos})

def editarAlumno(request):
    if request.method == "POST":
        matricula = request.POST['txtMatricula']
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        curp = request.POST['txtCurp']
        estado = request.POST['selectEstado']

        alumno = Alumno.objects.get(matricula=matricula)
        alumno.nombre = nombre
        alumno.correo = correo
        alumno.curp = curp
        alumno.estado = estado
        alumno.save()
    return redirect('nuevoalumno')

def eliminacionAlumno(request, matricula):
    alumno = get_object_or_404(Alumno, matricula=matricula)
    alumno.delete()
    return redirect('nuevoalumno')
