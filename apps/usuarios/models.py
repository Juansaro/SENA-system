from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=20,
        choices=[
            ('administrador', 'Administrador'),
            ('coordinador', 'Coordinador'),
            ('asesor', 'Asesor'),
            ('aprendiz', 'Aprendiz'),
        ],
        default='aprendiz',
    )
    es_valido = models.BooleanField(default=False)
    view_sensitive_data = models.BooleanField(default=False)

    class Meta:
        db_table = 'usuario'

    def clean(self):
        if self.rol not in dict(self.rol.choices).keys():
            raise ValidationError(f"El rol '{self.rol}' no es válido.")


class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'administrador'


class Coordinador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'coordinador'


class Asesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'asesor'


class Aprendiz(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('nuevo', 'Nuevo'),
            ('informado', 'Informado'),
            ('registrado', 'Registrado'),
        ],
        default='nuevo'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_informado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"

    def clean(self):
        #validar que  el correo que si este en lista blanca
        if not self.correo.endswith('@sena.edu.co'):
            raise ValidationError("El correo no está en la lista blanca.")


class Curso(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    creado_por = models.ForeignKey(Coordinador, on_delete=models.PROTECT, related_name='cursos_creados')

    class Meta:
        db_table = 'curso'


class Ficha(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='fichas')
    asesor = models.ForeignKey(Asesor, on_delete=models.SET_NULL, null=True, blank=True, related_name='fichas_asignadas')
    creado_por = models.ForeignKey(Coordinador, on_delete=models.PROTECT, related_name='fichas_creadas')

    class Meta:
        db_table = 'ficha'


class Documento(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE, related_name='documentos')
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE, related_name='documentos', null=True, blank=True)
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    tipo_documento = models.CharField(
        max_length=50,
        choices=[
            ('cedula', 'Cedula'),
            ('CedulaExtranjeria', 'CedulaExtranjeria'),
            ('Pasaporte', 'Pasaporte'),
        ]
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aprobado', 'Aprobado'),
            ('rechazado', 'Rechazado'),
        ],
        default='pendiente',
    )
    motivo_rechazo = models.TextField(null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='documentos_creados')
    modificado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_modificados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'documento'

    def clean(self):
        if not self.archivo.name.endswith(('.pdf', '.jpg', '.png')):
            raise ValidationError('El archivo debe ser de tipo PDF o imagen.')


class GestionDocumento(models.Model):
    documento = models.OneToOneField(Documento, on_delete=models.CASCADE)
    aprobado_por = models.ForeignKey(Asesor, on_delete=models.PROTECT, null=True, blank=True, related_name='documentos_aprobados')
    rechazado_por = models.ForeignKey(Asesor, on_delete=models.PROTECT, null=True, blank=True, related_name='documentos_rechazados')
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aprobado', 'Aprobado'),
            ('rechazado', 'Rechazado'),
        ],
        default='pendiente',
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    fecha_rechazo = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'gestion_documento'
