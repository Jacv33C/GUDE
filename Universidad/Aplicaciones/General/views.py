from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Alumno, Docente, Tarea
from django.http import JsonResponse
from django.contrib import messages
import random
from django.urls import reverse
from django import forms
import string
from django.db.models import Q
from django.utils import timezone
from .models import HistorialAcademico
from .forms import HistorialForm

from django.shortcuts import render, redirect, get_object_or_404

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
    alumno = None
    alumno_id = request.session.get("alumno_id")  # Obtienes la matrícula de sesión
    if alumno_id:
        alumno = Alumno.objects.filter(matricula=alumno_id).first()
    return render(request, "homebasealumnos.html", {'alumno': alumno})



def cargamateria(request):
    return render(request, "cargamateria.html")
from django.shortcuts import redirect

def cerrar_sesion(request):
    request.session.flush()  
    return redirect('login') 

def baseDocentes(request):
    return render(request, "baseDocentes.html")



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

from django.db import IntegrityError

def registrarAlumno(request):
    if request.method == "POST":
        matricula = request.POST['txtMatricula']
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        curp = request.POST['txtCurp']
        estado = request.POST['selectEstado']

        if Alumno.objects.filter(correo=correo).exists():
            messages.error(request, "Ya existe un alumno con ese correo.")
        else:
            try:
                Alumno.objects.create(
                    matricula=matricula,
                    nombre=nombre,
                    correo=correo,
                    curp=curp,
                    estado=estado
                )
                messages.success(request, "Alumno registrado exitosamente.")
            except IntegrityError:
                messages.error(request, "Ocurrió un error al registrar el alumno.")
    
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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno

def datosgeneralesalumnos(request):
    if request.session.get("tipo_usuario") != "alumno":
        return redirect('login')

    alumno_id = request.session.get("alumno_id")
    alumno = get_object_or_404(Alumno, matricula=alumno_id)

    return render(request, "datosgeneralesalumnos.html", {"alumno": alumno})
def cargar_materias_alumno(request):
    if request.session.get("tipo_usuario") != "alumno":
        return redirect('login')

    alumno_id = request.session.get("alumno_id")
    alumno = get_object_or_404(Alumno, matricula=alumno_id)

    # Materias disponibles para inscribirse: solo aquellas que tienen docentes asignados
    cursos_disponibles = Curso.objects.filter(docentes__isnull=False).exclude(alumnos=alumno).distinct()

    # Materias ya inscritas por el alumno
    cursos_inscritos = alumno.cursos.all()

    if request.method == 'POST':
        cursos_seleccionados = request.POST.getlist('cursos')
        for codigo in cursos_seleccionados:
            curso = get_object_or_404(Curso, codigo=codigo)
            alumno.cursos.add(curso)
        return redirect('cargar_materias_alumno')

    context = {
        'alumno': alumno,
        'cursos_disponibles': cursos_disponibles,
        'cursos_inscritos': cursos_inscritos,
    }
    return render(request, 'cargar_materias_alumno.html', context)
def inscribirMateriasAlumno(request):
    if request.session.get("tipo_usuario") != "alumno":
        return redirect('login')

    alumno_id = request.session.get("alumno_id")
    alumno = get_object_or_404(Alumno, matricula=alumno_id)

    if request.method == 'POST':
        cursos_seleccionados = request.POST.getlist('cursos')
        for codigo in cursos_seleccionados:
            curso = get_object_or_404(Curso, codigo=codigo)
            if curso not in alumno.cursos.all():
                alumno.cursos.add(curso)
        return redirect('inscribirMateriasAlumno')

    cursos_inscritos = alumno.cursos.all()
    cursos_disponibles = Curso.objects.exclude(
        codigo__in=cursos_inscritos.values_list('codigo', flat=True)
    )

    context = {
        'alumno': alumno,
        'cursos_disponibles': cursos_disponibles,
        'cursos_inscritos': cursos_inscritos,
    }

    return render(request, 'inscribirMateriasAlumno.html', context)
def ver_tareas_alumno(request, matricula):
    alumno = get_object_or_404(Alumno, matricula=matricula)
    cursos = alumno.cursos.all().prefetch_related('tareas')

    contexto = {
        'alumno': alumno,
        'cursos': cursos,
    }

    return render(request, 'TareasAlumnos.html', contexto)





# ---------------- CRUD DOCENTES ----------------

def generar_contrasena(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

def nuevodocente(request):
    docentes = Docente.objects.all()
    cursos = Curso.objects.all()  # Traer todas las materias
    return render(request, "nuevodocente.html", {"docentes": docentes, "cursos": cursos})

def buscar_materias(request):
    term = request.GET.get('term', '')
    cursos = Curso.objects.filter(nombre__icontains=term) | Curso.objects.filter(codigo__icontains=term)

    resultados = []
    for curso in cursos[:10]:  # máximo 10 sugerencias
        resultados.append({
            'label': f"{curso.nombre} ({curso.codigo})",  # lo que se muestra al usuario
            'value': curso.codigo  # lo que se guarda en el input
        })

    return JsonResponse(resultados, safe=False)

def registrarDocente(request):
    if request.method == "POST":
        id_docente = request.POST['txtId']
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        rfc = request.POST['txtRfc']

        docente = Docente(
            id=id_docente,
            nombre=nombre,
            correo=correo,
            rfc=rfc
        )
        docente.save()

        return redirect('nuevodocente')

    


def edicionDocente(request, id):
    docente = get_object_or_404(Docente, id=id)
    cursos = Curso.objects.all()
    return render(request, "edicionDocente.html", {"docente": docente, "cursos": cursos})

def editarDocente(request, id):
    if request.method == "POST":
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        especialidad = request.POST.get('txtEspecialidad', '')
        rfc = request.POST['txtRfc']

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

def detalle_docente(request, id):
    docente = get_object_or_404(Docente, id=id)
    return render(request, "detalle_docente.html", {"docente": docente})

def homebasedocentes(request):
    return render(request, 'homebasedocentes.html')

def verMateriasDocente(request):
    return render(request, 'verMateriasDocente.html')

# Aquí agrego la lógica para que "datosgeneralesdocentes" funcione igual que en alumnos:
def datosgeneralesdocentes(request):
    # Si no está logueado como docente, redirige a login (ajusta según tu sistema)
    if request.session.get("tipo_usuario") != "docente":
        return redirect('login')
    
    docente_id = request.session.get("docente_id")
    docente = get_object_or_404(Docente, id=docente_id)

    return render(request, 'datosgeneralesdocentes.html', {"docente": docente})



def asignarMaterias(request, docente_id):
    docente = get_object_or_404(Docente, pk=docente_id)

    if request.method == 'POST':
        cursos_seleccionados = request.POST.getlist('cursos')
        for codigo in cursos_seleccionados:
            curso = get_object_or_404(Curso, codigo=codigo)
            if curso not in docente.cursos.all():
                docente.cursos.add(curso)
        return redirect('asignarMaterias', docente_id=docente.id)

    cursos_asignados_a_otros = Curso.objects.filter(docentes__isnull=False).exclude(docentes=docente).distinct()
    cursos_asignados_al_docente = docente.cursos.all()

    cursos_disponibles = Curso.objects.exclude(
        codigo__in=cursos_asignados_a_otros.values_list('codigo', flat=True)
    ).exclude(
        codigo__in=cursos_asignados_al_docente.values_list('codigo', flat=True)
    )

    # Búsqueda por matrícula (código de curso)
    resultado_busqueda = None
    if 'buscar' in request.GET:
        codigo_busqueda = request.GET.get('buscar').strip()
        try:
            curso_encontrado = Curso.objects.get(codigo=codigo_busqueda)
            docentes_asignados = curso_encontrado.docentes.all()
            resultado_busqueda = {
                'curso': curso_encontrado,
                'docentes': docentes_asignados
            }
        except Curso.DoesNotExist:
            resultado_busqueda = {'error': 'No se encontró ninguna materia con esa matrícula.'}

    context = {
        'docente': docente,
        'cursos': cursos_disponibles,
        'cursos_docente': cursos_asignados_al_docente,
        'resultado_busqueda': resultado_busqueda,
    }

    return render(request, 'asignarMaterias.html', context)



def desasignar_materia(request, docente_id, codigo):
    docente = get_object_or_404(Docente, id=docente_id)
    curso = get_object_or_404(Curso, codigo=codigo)
    docente.cursos.remove(curso)
    return redirect('asignarMaterias', docente_id=docente.id)

def generar_id_aleatorio(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))
def guardardocente(request):
    if request.method == 'POST':
        nombre = request.POST.get('txtNombre')
        correo = request.POST.get('txtCorreo')
        especialidad = request.POST.get('txtEspecialidad', '')  # si existe en modelo
        rfc = request.POST.get('txtRfc')

        # Generar un id aleatorio o usar alguna lógica para el ID
        nuevo_id = generar_id_aleatorio(6)

        # Crear y guardar el docente
        docente = Docente(
            id=nuevo_id,
            nombre=nombre,
            correo=correo,
            rfc=rfc,
        )

        # Si tienes un campo especialidad en tu modelo Docente, asignarlo
        if hasattr(docente, 'especialidad'):
            docente.especialidad = especialidad

        docente.save()

        return redirect('nuevodocente')

    # Si se accede con GET o de forma incorrecta, redirigir a nuevodocente
    return redirect('nuevodocente')

def verMateriasDocente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    materias = docente.cursos.all()  # o el related_name que tengas

    return render(request, 'verMateriasDocente.html', {
        'docente': docente,
        'materias': materias
        
    })
def baseDocentes(request):
    docentes = Docente.objects.all()
    return render(request, 'baseDocentes.html', {'docentes': docentes})
def listarMateriasConTareas(request):
    # Validar que sea docente
    if request.session.get("tipo_usuario") != "docente":
        return redirect('login')

    docente_id = request.session.get("docente_id")
    docente = get_object_or_404(Docente, id=docente_id)

    # Obtener cursos con sus tareas
    cursos = docente.cursos.prefetch_related('tareas').all()

    # Renderizar template dentro de carpeta General
    return render(request, 'verMateriasDocente.html', {'docente': docente, 'cursos': cursos})



def agregarTarea(request, curso_codigo):
    curso = get_object_or_404(Curso, codigo=curso_codigo)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion', '')
        fecha_entrega_str = request.POST.get('fecha_entrega')

        if titulo and fecha_entrega_str:
            try:
                fecha_entrega = timezone.datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_entrega = timezone.now().date()

            Tarea.objects.create(
                curso=curso,
                titulo=titulo,
                descripcion=descripcion,
                fecha_entrega=fecha_entrega
            )

            docente_id = request.session.get('docente_id')
            if docente_id:
                return redirect('verMateriasDocente', docente_id=docente_id)
            else:
                return redirect('login')  # o una página de error

    return render(request, 'Tareas.html', {'curso': curso})



def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    tarea.delete()
    messages.success(request, "La tarea fue eliminada correctamente.")
    # Redirige a donde quieras después de eliminar, por ejemplo a la lista de materias o tareas
    return redirect('verMateriasDocente', request.session.get('docente_id'))
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'fecha_entrega', 'descripcion']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'})
        }

def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    
    # Supongamos que tienes una forma de obtener docente_id desde la tarea o sesión
    docente_id = request.session.get('docente_id', None)  # O como lo obtengas

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('verMateriasDocente', docente_id=docente_id)
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'EditarTareas.html', {
        'form': form,
        'tarea': tarea,
        'docente_id': docente_id  # aquí lo pasas para la plantilla
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Alumno, Docente, Tarea
from django.http import JsonResponse
from django.contrib import messages
import random
from django.urls import reverse
from django import forms
import string
from django.db.models import Q
from django.utils import timezone
from .models import HistorialAcademico
from .forms import HistorialForm

from django.shortcuts import render, redirect, get_object_or_404

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
    alumno = None
    alumno_id = request.session.get("alumno_id")  # Obtienes la matrícula de sesión
    if alumno_id:
        alumno = Alumno.objects.filter(matricula=alumno_id).first()
    return render(request, "homebasealumnos.html", {'alumno': alumno})



def cargamateria(request):
    return render(request, "cargamateria.html")
from django.shortcuts import redirect

def cerrar_sesion(request):
    request.session.flush()  
    return redirect('login') 

def baseDocentes(request):
    return render(request, "baseDocentes.html")



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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno

def datosgeneralesalumnos(request):
    if request.session.get("tipo_usuario") != "alumno":
        return redirect('login')

    alumno_id = request.session.get("alumno_id")
    alumno = get_object_or_404(Alumno, matricula=alumno_id)

    return render(request, "datosgeneralesalumnos.html", {"alumno": alumno})
def cargar_materias_alumno(request):
    if request.session.get("tipo_usuario") != "alumno":
        return redirect('login')

    alumno_id = request.session.get("alumno_id")
    alumno = get_object_or_404(Alumno, matricula=alumno_id)

    # Materias disponibles para inscribirse: solo aquellas que tienen docentes asignados
    cursos_disponibles = Curso.objects.filter(docentes__isnull=False).exclude(alumnos=alumno).distinct()

    # Materias ya inscritas por el alumno
    cursos_inscritos = alumno.cursos.all()

    if request.method == 'POST':
        cursos_seleccionados = request.POST.getlist('cursos')
        for codigo in cursos_seleccionados:
            curso = get_object_or_404(Curso, codigo=codigo)
            alumno.cursos.add(curso)
        return redirect('cargar_materias_alumno')

    context = {
        'alumno': alumno,
        'cursos_disponibles': cursos_disponibles,
        'cursos_inscritos': cursos_inscritos,
    }
    return render(request, 'cargar_materias_alumno.html', context)
def inscribirMateriasAlumno(request):
    if request.session.get("tipo_usuario") != "alumno":
        return redirect('login')

    alumno_id = request.session.get("alumno_id")
    alumno = get_object_or_404(Alumno, matricula=alumno_id)

    if request.method == 'POST':
        cursos_seleccionados = request.POST.getlist('cursos')
        for codigo in cursos_seleccionados:
            curso = get_object_or_404(Curso, codigo=codigo)
            if curso not in alumno.cursos.all():
                alumno.cursos.add(curso)
        return redirect('inscribirMateriasAlumno')

    cursos_inscritos = alumno.cursos.all()
    cursos_disponibles = Curso.objects.exclude(
        codigo__in=cursos_inscritos.values_list('codigo', flat=True)
    )

    context = {
        'alumno': alumno,
        'cursos_disponibles': cursos_disponibles,
        'cursos_inscritos': cursos_inscritos,
    }

    return render(request, 'inscribirMateriasAlumno.html', context)
def ver_tareas_alumno(request, matricula):
    alumno = get_object_or_404(Alumno, matricula=matricula)
    cursos = alumno.cursos.all().prefetch_related('tareas')

    contexto = {
        'alumno': alumno,
        'cursos': cursos,
    }

    return render(request, 'TareasAlumnos.html', contexto)





# ---------------- CRUD DOCENTES ----------------

def generar_contrasena(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

def nuevodocente(request):
    docentes = Docente.objects.all()
    cursos = Curso.objects.all()  # Traer todas las materias
    return render(request, "nuevodocente.html", {"docentes": docentes, "cursos": cursos})

def buscar_materias(request):
    term = request.GET.get('term', '')
    cursos = Curso.objects.filter(nombre__icontains=term) | Curso.objects.filter(codigo__icontains=term)

    resultados = []
    for curso in cursos[:10]:  # máximo 10 sugerencias
        resultados.append({
            'label': f"{curso.nombre} ({curso.codigo})",  # lo que se muestra al usuario
            'value': curso.codigo  # lo que se guarda en el input
        })

    return JsonResponse(resultados, safe=False)

def registrarDocente(request):
    if request.method == "POST":
        id_docente = request.POST['txtId']
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        rfc = request.POST['txtRfc']

        docente = Docente(
            id=id_docente,
            nombre=nombre,
            correo=correo,
            rfc=rfc
        )
        docente.save()

        return redirect('nuevodocente')

    


def edicionDocente(request, id):
    docente = get_object_or_404(Docente, id=id)
    cursos = Curso.objects.all()
    return render(request, "edicionDocente.html", {"docente": docente, "cursos": cursos})

def editarDocente(request, id):
    if request.method == "POST":
        nombre = request.POST['txtNombre']
        correo = request.POST['txtCorreo']
        especialidad = request.POST.get('txtEspecialidad', '')
        rfc = request.POST['txtRfc']

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

def detalle_docente(request, id):
    docente = get_object_or_404(Docente, id=id)
    return render(request, "detalle_docente.html", {"docente": docente})

def homebasedocentes(request):
    return render(request, 'homebasedocentes.html')

def verMateriasDocente(request):
    return render(request, 'verMateriasDocente.html')

# Aquí agrego la lógica para que "datosgeneralesdocentes" funcione igual que en alumnos:
def datosgeneralesdocentes(request):
    # Si no está logueado como docente, redirige a login (ajusta según tu sistema)
    if request.session.get("tipo_usuario") != "docente":
        return redirect('login')
    
    docente_id = request.session.get("docente_id")
    docente = get_object_or_404(Docente, id=docente_id)

    return render(request, 'datosgeneralesdocentes.html', {"docente": docente})



def asignarMaterias(request, docente_id):
    docente = get_object_or_404(Docente, pk=docente_id)

    if request.method == 'POST':
        cursos_seleccionados = request.POST.getlist('cursos')
        for codigo in cursos_seleccionados:
            curso = get_object_or_404(Curso, codigo=codigo)
            if curso not in docente.cursos.all():
                docente.cursos.add(curso)
        return redirect('asignarMaterias', docente_id=docente.id)

    cursos_asignados_a_otros = Curso.objects.filter(docentes__isnull=False).exclude(docentes=docente).distinct()
    cursos_asignados_al_docente = docente.cursos.all()

    cursos_disponibles = Curso.objects.exclude(
        codigo__in=cursos_asignados_a_otros.values_list('codigo', flat=True)
    ).exclude(
        codigo__in=cursos_asignados_al_docente.values_list('codigo', flat=True)
    )

    # Búsqueda por matrícula (código de curso)
    resultado_busqueda = None
    if 'buscar' in request.GET:
        codigo_busqueda = request.GET.get('buscar').strip()
        try:
            curso_encontrado = Curso.objects.get(codigo=codigo_busqueda)
            docentes_asignados = curso_encontrado.docentes.all()
            resultado_busqueda = {
                'curso': curso_encontrado,
                'docentes': docentes_asignados
            }
        except Curso.DoesNotExist:
            resultado_busqueda = {'error': 'No se encontró ninguna materia con esa matrícula.'}

    context = {
        'docente': docente,
        'cursos': cursos_disponibles,
        'cursos_docente': cursos_asignados_al_docente,
        'resultado_busqueda': resultado_busqueda,
    }

    return render(request, 'asignarMaterias.html', context)



def desasignar_materia(request, docente_id, codigo):
    docente = get_object_or_404(Docente, id=docente_id)
    curso = get_object_or_404(Curso, codigo=codigo)
    docente.cursos.remove(curso)
    return redirect('asignarMaterias', docente_id=docente.id)

def generar_id_aleatorio(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))
def guardardocente(request):
    if request.method == 'POST':
        nombre = request.POST.get('txtNombre')
        correo = request.POST.get('txtCorreo')
        especialidad = request.POST.get('txtEspecialidad', '')  # si existe en modelo
        rfc = request.POST.get('txtRfc')

        # Generar un id aleatorio o usar alguna lógica para el ID
        nuevo_id = generar_id_aleatorio(6)

        # Crear y guardar el docente
        docente = Docente(
            id=nuevo_id,
            nombre=nombre,
            correo=correo,
            rfc=rfc,
        )

        # Si tienes un campo especialidad en tu modelo Docente, asignarlo
        if hasattr(docente, 'especialidad'):
            docente.especialidad = especialidad

        docente.save()

        return redirect('nuevodocente')

    # Si se accede con GET o de forma incorrecta, redirigir a nuevodocente
    return redirect('nuevodocente')

def verMateriasDocente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    materias = docente.cursos.all()  # o el related_name que tengas

    return render(request, 'verMateriasDocente.html', {
        'docente': docente,
        'materias': materias
        
    })
def baseDocentes(request):
    docentes = Docente.objects.all()
    return render(request, 'baseDocentes.html', {'docentes': docentes})
def listarMateriasConTareas(request):
    # Validar que sea docente
    if request.session.get("tipo_usuario") != "docente":
        return redirect('login')

    docente_id = request.session.get("docente_id")
    docente = get_object_or_404(Docente, id=docente_id)

    # Obtener cursos con sus tareas
    cursos = docente.cursos.prefetch_related('tareas').all()

    # Renderizar template dentro de carpeta General
    return render(request, 'verMateriasDocente.html', {'docente': docente, 'cursos': cursos})



def agregarTarea(request, curso_codigo):
    curso = get_object_or_404(Curso, codigo=curso_codigo)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion', '')
        fecha_entrega_str = request.POST.get('fecha_entrega')

        if titulo and fecha_entrega_str:
            try:
                fecha_entrega = timezone.datetime.strptime(fecha_entrega_str, '%Y-%m-%d').date()
            except ValueError:
                fecha_entrega = timezone.now().date()

            Tarea.objects.create(
                curso=curso,
                titulo=titulo,
                descripcion=descripcion,
                fecha_entrega=fecha_entrega
            )

            docente_id = request.session.get('docente_id')
            if docente_id:
                return redirect('verMateriasDocente', docente_id=docente_id)
            else:
                return redirect('login')  # o una página de error

    return render(request, 'Tareas.html', {'curso': curso})



def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    tarea.delete()
    messages.success(request, "La tarea fue eliminada correctamente.")
    # Redirige a donde quieras después de eliminar, por ejemplo a la lista de materias o tareas
    return redirect('verMateriasDocente', request.session.get('docente_id'))
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'fecha_entrega', 'descripcion']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'})
        }

def editar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    
    # Supongamos que tienes una forma de obtener docente_id desde la tarea o sesión
    docente_id = request.session.get('docente_id', None)  # O como lo obtengas

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('verMateriasDocente', docente_id=docente_id)
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'EditarTareas.html', {
        'form': form,
        'tarea': tarea,
        'docente_id': docente_id  # aquí lo pasas para la plantilla
    })

# ---------------- CRUD HISTORIAL ACADÉMICO ----------------

def lista_historial(request):
    historial = HistorialAcademico.objects.all()
    return render(request, 'historial/listar.html', {'historial': historial})

def crear_historial(request):
    form = HistorialForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_historial')
    return render(request, 'historial/formulario.html', {'formulario': form, 'titulo': 'Agregar nuevo historial'})


def editar_historial(request, id):
    historial = get_object_or_404(HistorialAcademico, id=id)
    form = HistorialForm(request.POST or None, instance=historial)
    if form.is_valid():
        form.save()
        return redirect('lista_historial')
    return render(request, 'historial/formulario.html', {'formulario': form, 'titulo': 'Editar historial'})


def eliminar_historial(request, id):
    historial = get_object_or_404(HistorialAcademico, id=id)
    if request.method == 'POST':
        historial.delete()
        return redirect('lista_historial')
    return render(request, 'historial/eliminar.html', {'historial': historial})
