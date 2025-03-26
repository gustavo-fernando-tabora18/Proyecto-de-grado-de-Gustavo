from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class ModeloBase(models.Model):
    """
    Modelo base que incluye campos de seguimiento temporal y de usuario
    """
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    creado_por = models.ForeignKey(
        User,
        related_name='%(class)s_creados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False
    )
    actualizado_por = models.ForeignKey(
        User,
        related_name='%(class)s_actualizados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False
    )

    class Meta:
        abstract = True
        ordering = ['-creado_en']

class Empresa(ModeloBase):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()

    class Meta(ModeloBase.Meta):
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre

class Abanderado(ModeloBase):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Estacion(ModeloBase):
    nombre = models.CharField(max_length=255)
    ubicacion = models.TextField()
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    abanderado = models.ForeignKey(Abanderado, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.empresa})"

class Solicitante(ModeloBase):
    GENERO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro')
    ]

    dni = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    fecha_nacimiento = models.DateField()
    cv = models.FileField(upload_to='cvs/', max_length=255)
    foto = models.ImageField(upload_to='fotos/', max_length=255)
    direccion = models.TextField()
    vacante = models.ForeignKey('Vacante', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.vacante}"

class Vacante(ModeloBase):
    MODALIDAD_CHOICES = [
        ('Presencial', 'Presencial'),
        ('Remoto', 'Remoto'),
        ('Híbrido', 'Híbrido')
    ]
    TIPO_CONTRATO_CHOICES = [
        ('Tiempo completo', 'Tiempo completo'),
        ('Medio tiempo', 'Medio tiempo'),
        ('Temporal', 'Temporal')
    ]

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    numero_vacantes = models.PositiveIntegerField()
    nivel_experiencia = models.CharField(max_length=100)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    departamento = models.CharField(max_length=100)
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    fecha_maxima_postulacion = models.DateField()
    correo_contacto = models.EmailField()
    categoria = models.CharField(max_length=100)
    salario_ofrecido = models.DecimalField(max_digits=10, decimal_places=2)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estacion = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"

class Empleado(ModeloBase):
    TIPO_CONTRATO_CHOICES = [
        ('TIEMPO_COMPLETO', 'Tiempo completo'),
        ('MEDIO_TIEMPO', 'Medio tiempo'),
        ('TEMPORAL', 'Temporal')
    ]
    
    solicitante = models.OneToOneField(Solicitante, on_delete=models.CASCADE, related_name='empleado')
    fecha_contratacion = models.DateField()
    tipo_contrato = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estaciones = models.ManyToManyField(Estacion, through='AsignacionEstacion')

    def estacion_actual(self):
        asignacion = self.asignacionestacion_set.filter(fecha_finalizacion__isnull=True).first()
        return asignacion.estacion if asignacion else None

    def __str__(self):
        return f"{self.solicitante.nombre} - {self.empresa}"

class AsignacionEstacion(ModeloBase):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(default=timezone.now)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    es_responsable = models.BooleanField(default=False)

    class Meta(ModeloBase.Meta):
        ordering = ['-fecha_asignacion']

    def clean(self):
        if self.fecha_finalizacion and self.fecha_asignacion > self.fecha_finalizacion:
            raise ValidationError("La fecha de finalización no puede ser anterior a la de asignación")

    def __str__(self):
        return f"{self.empleado} en {self.estacion}"

class Entrevistador(ModeloBase):
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

class Entrevista(ModeloBase):
    MODALIDAD_CHOICES = [
        ('Presencial', 'Presencial'),
        ('Virtual', 'Virtual')
    ]
    ESTADO_CHOICES = [
        ('Programada', 'Programada'),
        ('Realizada', 'Realizada'),
        ('Cancelada', 'Cancelada')
    ]

    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    lugar = models.CharField(max_length=255)
    vacante = models.ForeignKey(Vacante, on_delete=models.CASCADE)
    entrevistador = models.ForeignKey(Entrevistador, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.asunto} - {self.fecha}"

class Auditoria(models.Model):
    ACCIONES = [
        ('C', 'Creación'),
        ('A', 'Actualización'),
        ('E', 'Eliminación'),
        ('L', 'Inicio de Sesión'),
        ('S', 'Cierre de Sesión'),
        ('I', 'Intento Fallido'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=1, choices=ACCIONES)
    modelo_afectado = models.CharField(max_length=50)
    id_objeto = models.CharField(max_length=20, null=True, blank=True)
    detalles = models.JSONField(default=dict)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'

    def __str__(self):
        return f"{self.get_accion_display()} - {self.modelo_afectado} - {self.usuario}"

class Informe(ModeloBase):
    nombre = models.CharField(max_length=255)
    numero_pedido = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.JSONField()

    def __str__(self):
        return f"{self.nombre} - {self.numero_pedido}"

class Beneficio(ModeloBase):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, related_name='beneficios')
    dias_base = models.PositiveIntegerField(default=30)
    dias_tomados = models.PositiveIntegerField(default=0)
    dias_pendientes = models.PositiveIntegerField(default=0)

    @property
    def saldo_disponible(self):
        return self.dias_base - self.dias_tomados

    def __str__(self):
        return f"Beneficios de {self.empleado}"

class SolicitudVacaciones(ModeloBase):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado')
    ]
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_solicitados = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')

    def clean(self):
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("Fecha de inicio no puede ser posterior a fecha final")
        
        if self.estado == 'Aprobado' and self.dias_solicitados > self.empleado.beneficios.saldo_disponible:
            raise ValidationError("Días solicitados exceden el saldo disponible")

    def save(self, *args, **kwargs):
        if self.estado == 'Aprobado' and not self.pk:
            self.empleado.beneficios.dias_tomados += self.dias_solicitados
            self.empleado.beneficios.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solicitud de {self.empleado} - {self.dias_solicitados} días"
    

#Loggin y usuario:
 