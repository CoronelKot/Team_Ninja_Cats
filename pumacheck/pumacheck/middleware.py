from django.http import HttpResponseServerError

class ManejoErroresConexionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Manejo de errores de conexión
            return HttpResponseServerError("Error de conexión con la base de datos o el servidor.")
        return response
