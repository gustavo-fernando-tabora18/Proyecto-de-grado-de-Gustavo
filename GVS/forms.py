import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Empresa, Abanderado, Estacion, Empleado, Solicitante, Vacante, Entrevistador, Entrevista, Informe

# ==================== VALIDACIONES ====================
def validate_min_length(value, min_length, error_message=None):
    if value is None:
        return value
    stripped = value.strip()
    if len(stripped) < min_length:
        raise ValidationError(error_message or f"Mínimo {min_length} caracteres")
    return stripped

def validate_name(value, field_name="Nombre", min_length=3):
    cleaned = validate_min_length(value, min_length, f"{field_name} debe tener al menos {min_length} caracteres")
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s\-.&]+$', cleaned):
        raise ValidationError(f"{field_name} contiene caracteres inválidos")
    return cleaned

def validate_phone(value, country_code='+504', format_example='+504 XXXX-XXXX'):
    if not value:
        return value
    
    cleaned = value.strip()
    regex = rf'^{re.escape(country_code)}[\s-]?\d{{4}}[\s-]?\d{{4}}$'
    
    if not re.match(regex, cleaned):
        raise ValidationError(f"Formato inválido. Use: {format_example}")
    
    digits = re.sub(r'[\s-]', '', cleaned)[len(country_code):]
    return f"{country_code} {digits[:4]}-{digits[4:8]}"

def validate_email_custom(value):
    cleaned = value.strip()
    try:
        validate_email(cleaned)
        user, domain = cleaned.split('@')
        if not re.match(r'^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$', domain):
            raise ValidationError("Dominio inválido")
        return cleaned
    except (ValueError, ValidationError):
        raise ValidationError("Correo electrónico inválido")
    

    

# ==================== FORMULARIOS ====================
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion', 'direccion', 'telefono', 'correo_electronico']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Petroservicios S.A.'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de actividades principales...'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección exacta con referencia'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+504 XXXX-XXXX'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@empresa.com'
            }),
        }

    def clean_nombre(self):
        return validate_name(self.cleaned_data['nombre'])

    def clean_telefono(self):
        return validate_phone(self.cleaned_data['telefono'])

class AbanderadoForm(forms.ModelForm):
    class Meta:
        model = Abanderado
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del abanderado'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información relevante sobre el abanderado...'
            }),
        }

class EstacionForm(forms.ModelForm):
    class Meta:
        model = Estacion
        fields = ['nombre', 'ubicacion', 'telefono', 'correo_electronico', 'empresa', 'abanderado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Estación Shell Centro'
            }),
            'ubicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ubicación geográfica exacta'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+504 XXXX-XXXX'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'estacion@empresa.com'
            }),
            'empresa': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Seleccione empresa...'
            }),
            'abanderado': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Seleccione abanderado...'
            }),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['solicitante', 'fecha_contratacion', 'tipo_contrato', 'empresa']
        widgets = {
            'solicitante': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Buscar solicitante...'
            }),
            'fecha_contratacion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'dd/mm/aaaa'
            }),
            'tipo_contrato': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Tipo de contrato'
            }),
            'empresa': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Buscar empresa...'
            }),
        }

class SolicitanteForm(forms.ModelForm):
    class Meta:
        model = Solicitante
        fields = ['dni', 'nombre', 'telefono', 'correo_electronico', 'edad', 
                'genero', 'fecha_nacimiento', 'cv', 'foto', 'direccion', 'vacante']
        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 0801-1990-12345'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+504 XXXX-XXXX'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad entre 18-100'
            }),
            'genero': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa'
            }),
            'vacante': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Buscar vacante...'
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

class VacanteForm(forms.ModelForm):
    class Meta:
        model = Vacante
        fields = ['nombre', 'descripcion', 'numero_vacantes', 'nivel_experiencia', 
                'modalidad', 'departamento', 'tipo_contrato', 'fecha_maxima_postulacion',
                'correo_contacto', 'categoria', 'salario_ofrecido', 'empresa', 'estacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Gerente de Estación'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del puesto...'
            }),
            'numero_vacantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2',
                'min': 1
            }),
            'nivel_experiencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Junior, Senior, etc.'
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Recursos Humanos, Operaciones'
            }),
            'tipo_contrato': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_maxima_postulacion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'correo_contacto': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'rh@empresa.com'
            }),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Técnico, Profesional'
            }),
            'salario_ofrecido': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'En Lempiras',
                'step': '0.01'
            }),
            'empresa': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Buscar empresa...'
            }),
            'estacion': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true',
                'title': 'Buscar estación...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuración de choices para campos que los tienen
        self.fields['modalidad'].choices = [('', 'Seleccione modalidad...')] + Vacante.MODALIDAD_CHOICES
        self.fields['tipo_contrato'].choices = [('', 'Seleccione tipo de contrato...')] + Vacante.TIPO_CONTRATO_CHOICES
        
        # Configuración de querysets para relaciones
        self.fields['empresa'].queryset = Empresa.objects.all()
        self.fields['estacion'].queryset = Estacion.objects.all()

class EntrevistadorForm(forms.ModelForm):
    class Meta:
        model = Entrevistador
        fields = ['nombre', 'cargo', 'telefono', 'correo_electronico']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Gerente de RH'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+504 XXXX-XXXX'
            }),
            'correo_electronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'entrevistador@empresa.com'
            }),
        }

class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = ['asunto', 'descripcion', 'fecha', 'modalidad', 'estado', 
                'lugar', 'vacante', 'entrevistador', 'solicitante']
        widgets = {
            'asunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Entrevista técnica para puesto de cajero'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalles de la entrevista...'
            }),
            'fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lugar': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección o enlace virtual'
            }),
            'vacante': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true'
            }),
            'entrevistador': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true'
            }),
            'solicitante': forms.Select(attrs={
                'class': 'form-select selectpicker',
                'data-live-search': 'true'
            }),
        }

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['nombre', 'numero_pedido', 'usuario', 'contenido']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del informe'
            }),
            'numero_pedido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Contenido detallado del informe...'
            }),
        }