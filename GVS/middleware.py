# middleware.py
from django.contrib.auth import get_user
from django.utils import timezone
from .models import Auditoria
import json
from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    """Middleware para redirigir a usuarios no autenticados al login."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Excluir rutas públicas
        excluded_paths = [settings.LOGIN_URL, '/static/', '/admin/']
        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in excluded_paths):
            return redirect(settings.LOGIN_URL)
        
        return self.get_response(request)

class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Registrar login/logout
        if request.path == '/login/' and response.status_code == 302:
            self.registrar_accion(request, 'L', 'Sesión', detalles={'username': request.POST.get('username')})
        elif request.path == '/logout/':
            self.registrar_accion(request, 'S', 'Sesión')
        
        return response

    def registrar_accion(self, request, accion, modelo_afectado, id_objeto=None, detalles=None):
        user = request.user if request.user.is_authenticated else None
        detalles = detalles or {}
        
        Auditoria.objects.create(
            usuario=user,
            accion=accion,
            modelo_afectado=modelo_afectado,
            id_objeto=str(id_objeto) if id_objeto else None,
            detalles=detalles,
            ip=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip