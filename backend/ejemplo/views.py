from rest_framework.views import APIView
from django.http import HttpResponse

# Create your views here.

class Class_Ejemplo(APIView):

    def get(self, request):
        return HttpResponse("Hola ejemplo")