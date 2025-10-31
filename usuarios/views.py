from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UsuarioForm
from .models import Usuario  # ✅ precisa importar aqui
from .forms import UsuarioCreationForm  # <-- importa o certo
from usuarios.models import Perfil


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            # Cria o usuário
            user = form.save(commit=False)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.is_staff = user.is_superuser
            user.shopping = form.cleaned_data.get('shopping')
            user.save()

            # Agora associa o grupo
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                user.groups.add(grupo)  # ✅ adiciona
                user.save()

            # 🔥 Forçar busca atualizada do banco para ver grupo real
            user_atualizado = Usuario.objects.get(pk=user.pk)

            # Se é gestor, cria o perfil
            if user_atualizado.groups.filter(name="Gestor").exists():
                Perfil.objects.get_or_create(usuario=user_atualizado, defaults={'shopping': user_atualizado.shopping})

            messages.success(request, "Usuário criado com sucesso!")
            return redirect('listar_usuarios')
        else:
            messages.error(request, "Corrija os erros do formulário.")
    else:
        form = UsuarioCreationForm()

    return render(request, 'usuarios/criar_usuario.html', {'form': form})