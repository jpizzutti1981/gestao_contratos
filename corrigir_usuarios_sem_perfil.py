# corrigir_usuarios_sem_perfil.py

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_contratos.settings')
django.setup()

from usuarios.models import Usuario, Perfil

usuarios = Usuario.objects.all()

for usuario in usuarios:
    if not hasattr(usuario, 'perfil'):
        if usuario.groups.filter(name='Gestor').exists():
            Perfil.objects.create(usuario=usuario, shopping=usuario.shopping)
            print(f"Perfil criado para o Gestor: {usuario.username}")
        else:
            print(f"Usuário {usuario.username} não é gestor — sem perfil.")
