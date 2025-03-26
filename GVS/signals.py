# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Auditoria
import json

@receiver(post_save)
def registrar_creacion_actualizacion(sender, instance, created, **kwargs):
    if sender.__name__ == 'Auditoria' or sender.__name__ == get_user_model().__name__:
        return
    
    accion = 'C' if created else 'A'
    detalles = {
        'campos': {field.name: str(getattr(instance, field.name)) 
                 for field in instance._meta.fields}
    }
    
    Auditoria.objects.create(
        usuario=getattr(instance, 'usuario_creacion', None),
        accion=accion,
        modelo_afectado=sender.__name__,
        id_objeto=instance.pk,
        detalles=detalles
    )

@receiver(post_delete)
def registrar_eliminacion(sender, instance, **kwargs):
    if sender.__name__ == 'Auditoria' or sender.__name__ == get_user_model().__name__:
        return
    
    detalles = {
        'campos': {field.name: str(getattr(instance, field.name)) 
                 for field in instance._meta.fields}
    }
    
    Auditoria.objects.create(
        usuario=getattr(instance, 'usuario_ultima_modificacion', None),
        accion='E',
        modelo_afectado=sender.__name__,
        id_objeto=instance.pk,
        detalles=detalles
    )