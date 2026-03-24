from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.core.cache import cache
import time


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect('/login/')
            elif not request.user.is_staff:
                messages.error(request, 'No tienes permisos para acceder al panel de administración')
                return redirect('/')

        response = self.get_response(request)
        return response


class RateLimitMiddleware:
    """Limita intentos en rutas sensibles: login y procesar_pago."""
    LIMITS = {
        '/login/': (10, 300),       # 10 intentos cada 5 min
        '/procesar-pago/': (5, 60), # 5 intentos por minuto
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path in self.LIMITS:
            max_attempts, window = self.LIMITS[request.path]
            ip = self._get_ip(request)
            key = f'rl:{request.path}:{ip}'
            attempts = cache.get(key, 0)
            if attempts >= max_attempts:
                return HttpResponseForbidden('Demasiados intentos. Intenta más tarde.')
            cache.set(key, attempts + 1, window)

        return self.get_response(request)

    def _get_ip(self, request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')