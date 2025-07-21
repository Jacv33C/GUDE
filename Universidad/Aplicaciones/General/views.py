from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso


from django.shortcuts import render, redirect

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Verificamos si coincide con los datos "duros"
        if username == "jacvpa33personal@gmail.com" and password == "001122":
            return redirect('home')
        else:
            error = "Usuario o contraseña incorrectos."

    return render(request, "login.html", {"error": error})


def home(request):
    return render(request, "home.html")


def materias(request):
    return render(request, "materias.html")

def registrarMateria(request):
    return render(request, "registrarMateria.html")

def eliminacionCurso(request, codigo):
    return render(request, "eliminacionCurso.html", {"codigo": codigo})

def edicionCurso(request, codigo):
    return render(request, "edicionCurso.html", {"codigo": codigo})

def editarMateria(request):
    return render(request, "editarMateria.html")


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
