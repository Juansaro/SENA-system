from django.contrib.auth.models import Group

groups = ['Administrador', 'Coordinador', 'Asesor', 'Aprendiz']

for group_name in groups:
    Group.objects.get_or_create(name=group_name)

print("Grupos creados exitosamente.")