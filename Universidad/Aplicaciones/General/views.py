from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Alumno, Docente

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ADMINISTRADOR
        if username == "jacvpa33@gmail.com" and password == "001122":
            request.session["tipo_usuario"] = "admin"
            request.session["nombre"] = "Administrador"
            return redirect('home')

        # ALUMNO
        try:
            alumno = Alumno.objects.get(correo=username)
            if alumno.matricula == password:
                if alumno.estado != "activo":
                    error = "El alumno no está activo"
                else:
                    request.session["tipo_usuario"] = "alumno"
                    request.session["alumno_id"] = alumno.matricula
                    request.session["nombre"] = alumno.nombre
                    return redirect('baseAlumnos')
            else:
                error = "Contraseña incorrecta"
            return render(request, "login.html", {"error": error})
        except Alumno.DoesNotExist:
            pass  # Sigue intentando como docente

        # DOCENTE
        try:
            docente = Docente.objects.get(correo=username)
            if docente.rfc == password:
                request.session["tipo_usuario"] = "docente"
                request.session["docente_id"] = docente.id
                request.session["nombre"] = docente.nombre
                return redirect('baseDocentes')
            else:
                error = "Contraseña incorrecta"
        except Docente.DoesNotExist:
            error = "No existe un usuario con ese correo"

    return render(request, "login.html", {"error": error})


# ---------------- VISTAS PRINCIPALES ----------------
def home(request):
    return render(request, "home.html")

def baseAlumnos(request):
    return render(request, "BaseAlumnos.html")

def homebasealumnos(request):
    return render(request, "homebasealumnos.html")

def cargamateria(request):
    return render(request, "cargamateria.html")
from django.shortcuts import redirect

def cerrar_sesion(request):
    request.session.flush()  
    return redirect('login') 



# ---------------- CRUD MATERIAS ----------------
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


# ---------------- CRUD ALUMNOS ----------------
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

def datosgeneralesalumnos(request):
    return render(request, "datosgeneralesalumnos.html")


# ---------------- CRUD DOCENTES ----------------

def nuevodocente(request):
    docentes = Docente.objects.all()
    cursos = Curso.objects.all()  # Traer todas las materias
    return render(request, "nuevodocente.html", {"docentes": docentes, "cursos": cursos})

def registrarDocente(request):
    if request.method == "POST":
        id = request.POST['txtId']
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        especialidad = request.POST.get('txtEspecialidad', '')
        rfc = request.POST['txtRfc']
        Docente.objects.create(
            id=id,
            nombre=nombre,
            correo=correo,
            especialidad=especialidad,
            rfc=rfc
        )
    return redirect('nuevodocente')

def edicionDocente(request, id):
    docente = get_object_or_404(Docente, id=id)
    docentes = Docente.objects.all()
    return render(request, "edicionDocente.html", {"docente": docente, "docentes": docentes})

def editarDocente(request, id):
    if request.method == "POST":
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        especialidad = request.POST.get('txtEspecialidad', '')
        rfc = request.POST['txtRFC']  # <-- Aquí debe coincidir el nombre con el formulario

        docente = get_object_or_404(Docente, id=id)
        docente.nombre = nombre
        docente.correo = correo
        docente.especialidad = especialidad
        docente.rfc = rfc
        docente.save()

    return redirect('nuevodocente')



def eliminacionDocente(request, id):
    docente = get_object_or_404(Docente, id=id)
    docente.delete()
    return redirect('nuevodocente')
