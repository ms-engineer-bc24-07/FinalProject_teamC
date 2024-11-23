from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, Connetto!"})

def home_view(request):
    return HttpResponse("<h1>Welcome to Connetto Backend</h1>")