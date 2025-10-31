from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from documentos.models import RegistroDocumento  # substitui Documento e Contrato

def setup_grupos():
    # Criar grupos
    corporativo, _ = Group.objects.get_or_create(name='Corporativo')
    gestor, _ = Group.objects.get_or_create(name='Gestor')
    usuario, _ = Group.objects.get_or_create(name='Usuario')

    # Obter ContentType da nova model unificada
    registro_content = ContentType.objects.get_for_model(RegistroDocumento)

    # Todas permissões da model RegistroDocumento
    permissoes_basicas = Permission.objects.filter(content_type=registro_content)

    # Grupo Corporativo recebe todas
    corporativo.permissions.set(permissoes_basicas)

    # Gestor pode ver, aprovar, mas não deletar
    permissoes_gestor = permissoes_basicas.exclude(codename__startswith='delete')
    gestor.permissions.set(permissoes_gestor)

    # Usuário pode apenas adicionar e ver
    permissoes_usuario = permissoes_basicas.filter(
        codename__in=['add_registrodocumento', 'view_registrodocumento']
    )
    usuario.permissions.set(permissoes_usuario)

    print("✅ Grupos e permissões criados com sucesso.")
