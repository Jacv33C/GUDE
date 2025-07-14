from django.http import HttpResponse

def GUDE_Inicio(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>GUDE</title>
            <style>
                body {
                    margin: 0;
                    font-family: Arial, sans-serif;
                }

                .navbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    background-color: #2c3e50;
                    padding: 10px 20px;
                    color: white;
                }

                .navbar .title {
                    font-size: 24px;
                    font-weight: bold;
                }

                .navbar .links a {
                    color: white;
                    text-decoration: none;
                    margin-left: 20px;
                    font-size: 16px;
                }

                .navbar .links a:hover {
                    text-decoration: underline;
                }

                .content {
                    padding: 20px;
                }
            </style>
        </head>
        <body>

            <!-- Navbar -->
            <div class="navbar">
                <div class="title">GUDE</div>
                <div class="links">
                    <a href="#">Iniciar Sesion</a>
                    <a href="#">Registrar</a>
                    <a href="#">Contactos</a>
                    <a href="#">Alumnos</a>
                    <a href="#">Materias</a>
                </div>
            </div>

            <!-- Contenido -->
            <div class="content">
                <h1>Bienvenido a GUDE</h1>
            </div>

        </body>
        </html>
    """)
