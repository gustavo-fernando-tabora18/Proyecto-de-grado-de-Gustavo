# GVS/views.py
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse

from django.utils import timezone
from datetime import timedelta, datetime
import csv
import json
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import *
from .forms import *
from .mixins import SuccessMessageMixin, DeleteMessageMixin  # Importar los mixins
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder

def index(request):
    return render(request, 'base.html')

# EMPRESA
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'GVS/empresa/index.html'
    context_object_name = 'empresas'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Empresas')
        return context

class EmpresaCreateView(SuccessMessageMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'GVS/empresa/crear.html'
    success_url = reverse_lazy('GVS:empresa_list')
    success_message = "Empresa creada exitosamente!"

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'empresa': {
                    'id': self.object.id,
                    'nombre': str(self.object),
                    'texto': f"{self.object.nombre} (ID: {self.object.id})"
                }
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': form.errors.as_text()
            }, status=400)
        return super().form_invalid(form)


class EmpresaUpdateView(SuccessMessageMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'GVS/empresa/Editar.html'
    success_url = reverse_lazy('GVS:empresa_list')
    success_message = _('¡Cambios en "%(object)s" guardados correctamente!')

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'GVS/empresa/Eliminar.html'
    success_url = reverse_lazy('GVS:empresa_list')
    
    def get_success_message(self, cleaned_data):
        return _('¡Empresa "%(object)s" eliminada con éxito!')

# ABANDERADO
class AbanderadoListView(ListView):
    model = Abanderado
    template_name = 'GVS/abanderado/index.html'
    context_object_name = 'abanderados'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Abanderados')
        return context

class AbanderadoCreateView(SuccessMessageMixin, CreateView):
    model = Abanderado
    form_class = AbanderadoForm
    template_name = 'GVS/abanderado/crear.html'
    success_url = reverse_lazy('GVS:abanderado_list')
    success_message = "Abanderado creado exitosamente!"

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'abanderado': {
                    'id': self.object.id,
                    'nombre': self.object.nombre,  # Se eliminó 'apellido'
                    'texto': self.object.nombre
                }
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            }, status=400)
        return super().form_invalid(form)

class AbanderadoUpdateView(SuccessMessageMixin, UpdateView):
    model = Abanderado
    form_class = AbanderadoForm
    template_name = 'GVS/abanderado/Editar.html'
    success_url = reverse_lazy('GVS:abanderado_list')
    success_message = _('¡Cambios en "%(object)s" guardados correctamente!')

class AbanderadoDeleteView(DeleteView):
    model = Abanderado
    template_name = 'GVS/abanderado/Eliminar.html'
    success_url = reverse_lazy('GVS:abanderado_list')
    
    def get_success_message(self, cleaned_data):
        return _('¡Abanderado "%(object)s" eliminado con éxito!')

# ESTACION
class EstacionListView(ListView):
    model = Estacion
    template_name = 'GVS/estacion/index.html'
    context_object_name = 'estaciones'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Estaciones')
        return context

class EstacionCreateView(SuccessMessageMixin, CreateView):
    model = Estacion
    form_class = EstacionForm
    template_name = 'GVS/estacion/crear.html'
    success_url = reverse_lazy('GVS:estacion_list')
    success_message = "Estación creada exitosamente!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_form'] = EmpresaForm()  # Formulario para modal
        context['abanderado_form'] = AbanderadoForm()  # Formulario para modal
        return context

class EstacionUpdateView(SuccessMessageMixin, UpdateView):
    model = Estacion
    form_class = EstacionForm
    template_name = 'GVS/estacion/Editar.html'
    success_url = reverse_lazy('GVS:estacion_list')
    success_message = _('¡Estación "%(object)s" actualizada correctamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_form'] = EmpresaForm()
        context['abanderado_form'] = AbanderadoForm()
        return context

class EstacionDeleteView(DeleteView):
    model = Estacion
    template_name = 'GVS/estacion/Eliminar.html'
    success_url = reverse_lazy('GVS:estacion_list')
    
    def get_success_message(self, cleaned_data):
        return _('¡Estación "%(object)s" eliminada con éxito!')

# EMPLEADO
class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'GVS/empleado/index.html'
    context_object_name = 'empleados'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Empleados')
        return context

class EmpleadoCreateView(SuccessMessageMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'GVS/empleado/Crear.html'
    success_url = reverse_lazy('GVS:empleado_list')
    success_message = _('¡Empleado "%(object)s" creado exitosamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitante_form'] = SolicitanteForm()
        context['empresa_form'] = EmpresaForm()
        return context

class EmpleadoUpdateView(SuccessMessageMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'GVS/empleado/Editar.html'
    success_url = reverse_lazy('GVS:empleado_list')
    success_message = _('¡Empleado "%(object)s" actualizado correctamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solicitante_form'] = SolicitanteForm()
        context['empresa_form'] = EmpresaForm()
        return context

class EmpleadoDeleteView(DeleteMessageMixin, DeleteView):
    model = Empleado
    template_name = 'GVS/empleado/Eliminar.html'
    success_url = reverse_lazy('GVS:empleado_list')
    delete_success_message = _('¡Empleado "%(object)s" eliminado con éxito!')

# SOLICITANTE
class SolicitanteListView(ListView):
    model = Solicitante
    template_name = 'GVS/solicitante/index.html'
    context_object_name = 'solicitantes'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Solicitantes')
        return context

class SolicitanteCreateView(SuccessMessageMixin, CreateView):
    model = Solicitante
    form_class = SolicitanteForm
    template_name = 'GVS/solicitante/Crear.html'
    success_url = reverse_lazy('GVS:solicitante_list')
    success_message = _('¡Solicitante "%(object)s" creado exitosamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacante_form'] = VacanteForm()  # Añadir formulario de vacante al contexto
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'solicitante': {
                    'id': self.object.id,
                    'nombre': str(self.object)
                }
            })
        return super().form_valid(form)

class SolicitanteUpdateView(SuccessMessageMixin, UpdateView):
    model = Solicitante
    form_class = SolicitanteForm
    template_name = 'GVS/solicitante/Editar.html'
    success_url = reverse_lazy('GVS:solicitante_list')
    success_message = _('¡Solicitante "%(object)s" actualizado correctamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacante_form'] = VacanteForm()  # Añadir formulario de vacante al contexto
        return context

class SolicitanteDeleteView(DeleteMessageMixin, DeleteView):
    model = Solicitante
    template_name = 'GVS/solicitante/Eliminar.html'
    success_url = reverse_lazy('GVS:solicitante_list')
    delete_success_message = _('¡Solicitante "%(object)s" eliminado con éxito!')

# VACANTE
class VacanteListView(ListView):
    model = Vacante
    template_name = 'GVS/vacante/index.html'
    context_object_name = 'vacantes'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Vacantes')
        return context

class VacanteCreateView(SuccessMessageMixin, CreateView):
    model = Vacante
    form_class = VacanteForm
    template_name = 'GVS/vacante/Crear.html'
    success_url = reverse_lazy('GVS:vacante_list')
    success_message = _('¡Vacante "%(object)s" creada exitosamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_form'] = EmpresaForm()  # Añadir formulario de empresa
        context['estacion_form'] = EstacionForm()  # Añadir formulario de estación
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'vacante': {
                    'id': self.object.id,
                    'nombre': self.object.nombre,
                    'empresa': str(self.object.empresa) if self.object.empresa else '',
                    'estacion': str(self.object.estacion) if self.object.estacion else ''
                }
            })
        return super().form_valid(form)

class VacanteUpdateView(SuccessMessageMixin, UpdateView):
    model = Vacante
    form_class = VacanteForm
    template_name = 'GVS/vacante/Editar.html'
    success_url = reverse_lazy('GVS:vacante_list')
    success_message = _('¡Vacante "%(object)s" actualizada correctamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa_form'] = EmpresaForm()  # Añadir formulario de empresa
        context['estacion_form'] = EstacionForm()  # Añadir formulario de estación
        return context

class VacanteDeleteView(DeleteMessageMixin, DeleteView):
    model = Vacante
    template_name = 'GVS/vacante/Eliminar.html'
    success_url = reverse_lazy('GVS:vacante_list')
    delete_success_message = _('¡Vacante "%(object)s" eliminada con éxito!')

# ENTREVISTADOR
class EntrevistadorListView(ListView):
    model = Entrevistador
    template_name = 'GVS/entrevistador/index.html'
    context_object_name = 'entrevistadores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Entrevistadores')
        return context

class EntrevistadorCreateView(SuccessMessageMixin, CreateView):
    model = Entrevistador
    form_class = EntrevistadorForm
    template_name = 'GVS/entrevistador/Crear.html'
    success_url = reverse_lazy('GVS:entrevistador_list')
    success_message = _('¡Entrevistador "%(object)s" creado exitosamente!')

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'entrevistador': {
                    'id': self.object.id,
                    'nombre': self.object.nombre
                }
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)
        return super().form_invalid(form)


class EntrevistadorUpdateView(SuccessMessageMixin, UpdateView):
    model = Entrevistador
    form_class = EntrevistadorForm
    template_name = 'GVS/entrevistador/Editar.html'
    success_url = reverse_lazy('GVS:entrevistador_list')
    success_message = _('¡Entrevistador "%(object)s" actualizado correctamente!')

class EntrevistadorDeleteView(DeleteMessageMixin, DeleteView):
    model = Entrevistador
    template_name = 'GVS/entrevistador/Eliminar.html'
    success_url = reverse_lazy('GVS:entrevistador_list')
    delete_success_message = _('¡Entrevistador "%(object)s" eliminado con éxito!')

# ENTREVISTA
class EntrevistaListView(ListView):
    model = Entrevista
    template_name = 'GVS/entrevista/index.html'
    context_object_name = 'entrevistas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Entrevistas')
        return context

class EntrevistaCreateView(SuccessMessageMixin, CreateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'GVS/entrevista/Crear.html'
    success_url = reverse_lazy('GVS:entrevista_list')
    success_message = _('¡Entrevista creada exitosamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entrevistador_form'] = EntrevistadorForm()
        context['vacante_form'] = VacanteForm()
        context['solicitante_form'] = SolicitanteForm()
        return context

class EntrevistaUpdateView(SuccessMessageMixin, UpdateView):
    model = Entrevista
    form_class = EntrevistaForm
    template_name = 'GVS/entrevista/Editar.html'
    success_url = reverse_lazy('GVS:entrevista_list')
    success_message = _('¡Entrevista actualizada correctamente!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entrevistador_form'] = EntrevistadorForm()
        return context

class EntrevistaDeleteView(DeleteMessageMixin, DeleteView):
    model = Entrevista
    template_name = 'GVS/entrevista/Eliminar.html'
    success_url = reverse_lazy('GVS:entrevista_list')
    delete_success_message = _('¡Entrevista eliminada con éxito!')

# AUDITORIA
class AuditoriaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Auditoria
    template_name = 'auditoria/index.html'
    context_object_name = 'registros'
    paginate_by = 25
    permission_required = 'auth.view_user'  # O el permiso que prefieras

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros opcionales
        if 'modelo' in self.request.GET:
            queryset = queryset.filter(modelo_afectado=self.request.GET['modelo'])
        if 'usuario' in self.request.GET:
            queryset = queryset.filter(usuario__username=self.request.GET['usuario'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modelos'] = Auditoria.objects.values_list('modelo_afectado', flat=True).distinct()

        return context
# INFORME
class InformeListView(ListView):
    model = Informe
    template_name = 'GVS/informe/index.html'
    context_object_name = 'informes'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Listado de Informes')
        return context

class InformeCreateView(SuccessMessageMixin, CreateView):
    model = Informe
    form_class = InformeForm
    template_name = 'GVS/informe/Crear.html'
    success_url = reverse_lazy('GVS:informe_list')
    success_message = _('¡Informe "%(object)s" creado exitosamente!')

class InformeUpdateView(SuccessMessageMixin, UpdateView):
    model = Informe
    form_class = InformeForm
    template_name = 'GVS/informe/Editar.html'
    success_url = reverse_lazy('GVS:informe_list')
    success_message = _('¡Informe "%(object)s" actualizado correctamente!')

class InformeDeleteView(DeleteMessageMixin, DeleteView):
    model = Informe
    template_name = 'GVS/informe/Eliminar.html'
    success_url = reverse_lazy('GVS:informe_list')
    delete_success_message = _('¡Informe "%(object)s" eliminado con éxito!')



 #usuarios y loggin   
 