from django.urls import path
from .views import *

urlpatterns = [
    path('ejemplo', Class_Ejemplo.as_view())
]