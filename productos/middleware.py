from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar acceso al admin
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect('/login/')
            elif not request.user.is_staff:
                messages.error(request, 'No tienes permisos para acceder al panel de administración')
                return redirect('/')
        
        response = self.get_response(request)
        return response