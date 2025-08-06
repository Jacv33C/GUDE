Guia de DJANGO


Primero, tennemos que tener instalado Python y pip. Lo ideal es crear un entorno virtual para manejar las dependencias del proyecto.

Luego, instalo Django usando pip con el comando pip install django. Para verificar que se instaló bien, uso django-admin --version.

Después, creo un nuevo proyecto Django con django-admin startproject nombre_proyecto. Entro a la carpeta del proyecto con cd nombre_proyecto.

Dentro del proyecto, creo una app con python manage.py startapp nombre_app.

Registro la app que creé dentro del archivo settings.py, agregándola en la lista INSTALLED_APPS.

Ahora puedo crear las vistas en el archivo views.py de la app, definir las URLs en urls.py de la app y conectar esas URLs en el archivo urls.py principal del proyecto.

Luego, ejecuto las migraciones iniciales con python manage.py migrate para crear las tablas básicas en la base de datos.

Si quiero usar el panel admin, creo un superusuario con python manage.py createsuperuser y sigo las instrucciones.

Finalmente, corro el servidor de desarrollo con python manage.py runserver y abro el navegador en la dirección http://127.0.0.1:8000/ para ver mi app funcionando.

Para trabajar más, si hago cambios en los modelos, creo migraciones con python manage.py makemigrations y las aplico con python manage.py migrate.

También puedo usar python manage.py shell para entrar a una consola interactiva de Django y probar cosas rápido.

Como entrar al admin 
Correo jacvpa33@gmail.com -- pass 001122
Como entrar a los Docentes
Todos los docentes podran entrar con el correo dado a la administracion y su RFC
Como entar como estudiante
Los estudiantes podran entrar por medio de su Correo dado a la administracion y su Matricula
