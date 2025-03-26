# GVS/mixins.py
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from .models import Auditoria

class SuccessMessageMixin:
    """
    Mixin para manejar mensajes de éxito en CreateView y UpdateView
    """
    success_message = ""
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(
                self.request, 
                self.success_message % {
                    'object': self.object,
                    'model': self.model._meta.verbose_name
                }
            )
        return response

class DeleteMessageMixin:
    """
    Mixin para manejar mensajes de éxito en DeleteView
    """
    delete_success_message = ""
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().delete(request, *args, **kwargs)
        if self.delete_success_message:
            messages.success(
                request, 
                self.delete_success_message % {
                    'object': obj,
                    'model': self.model._meta.verbose_name
                }
            )
        return response
    

User = get_user_model()

class AuditoriaMixin:
    def registrar_auditoria(self, accion, instance, request=None):
        user = request.user if request and request.user.is_authenticated else None
        detalles = {
            'campos': self.obtener_detalles_campos(instance)
        }
        
        Auditoria.objects.create(
            usuario=user,
            accion=accion,
            modelo_afectado=instance.__class__.__name__,
            id_objeto=str(instance.pk),
            detalles=detalles,
            ip=self.get_client_ip(request),
            user_agent=self.get_user_agent(request)
        )
    
    def obtener_detalles_campos(self, instance):
        return {
            field.name: str(getattr(instance, field.name))
            for field in instance._meta.fields
            if field.name not in ['password', 'creado_en', 'actualizado_en']
        }
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_user_agent(self, request):
        return request.META.get('HTTP_USER_AGENT', '')