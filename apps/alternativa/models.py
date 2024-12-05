from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group



class Usuario(AbstractUser):
    es_administrador = models.BooleanField(default=False)
    es_coordinador = models.BooleanField(default=False)
    es_aprendiz = models.BooleanField(default=False)
    es_asesor = models.BooleanField(default=False)
    es_valido = models.BooleanField(default=False)

    class Meta:
        db_table = 'usuario'


    def get_administrador_profile(self):
        perfil_administrador = None
        if hasattr(self, 'perfiladministrador'):
            perfil_administrador = self.perfiladministrador
        return perfil_administrador


    def get_coordinador_profile(self):
        perfil_coordinador = None
        if hasattr(self, 'perfilcoordinador'):
            perfil_coordinador = self.perfilcoordinador
        return perfil_coordinador


    def get_asesor_profile(self):
        perfil_asesor = None
        if hasattr(self, 'perfilasesor'):
            perfil_asesor = self.perfilasesor
        return perfil_asesor


    def get_aprendiz_profile(self):
        perfil_aprendiz = None
        if hasattr(self, 'perfilaprendiz'):
            perfil_aprendiz = self.perfil_aprendiz
        return perfil_aprendiz

    # def save(self,*args,**kwargs):
    #     if not self.id:
    #         super().save(*args,**kwargs)
    #         grupo = Group.objects.get(name = 'perfilnormal')
    #         if grupo:
    #             self.groups.add(grupo)
    #         super().save(*args,**kwargs)


class UsuarioAdministrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class UsuarioCoordinador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class UsuarioAsesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class UsuarioAprendiz(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)



