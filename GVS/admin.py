from django.contrib import admin
from .models import (
    Empresa, Estacion, Abanderado, Empleado, AsignacionEstacion,
    Vacante, Solicitante, Entrevistador, Entrevista, Auditoria, Informe,
      
    Beneficio, SolicitudVacaciones
)

# Registro básico de modelos
admin.site.register(Empresa)
admin.site.register(Estacion)
admin.site.register(Abanderado)
admin.site.register(Empleado)
admin.site.register(AsignacionEstacion)
admin.site.register(Vacante)
admin.site.register(Solicitante)
admin.site.register(Entrevistador)
admin.site.register(Entrevista)

admin.site.register(Auditoria)
admin.site.register(Informe)



admin.site.register(Beneficio)
admin.site.register(SolicitudVacaciones)