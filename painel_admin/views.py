from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.contrib import messages

from documentos.models import Shopping
from usuarios.models import Usuario, Perfil
from usuarios.forms import UsuarioCreationForm
from .forms import ShoppingForm, UsuarioForm, UsuarioEditForm, PerfilForm

def is_superuser(user):
    return user.is_superuser

def is_corporativo(user):
    return user.groups.filter(name='Corporativo').exists()

@login_required
@user_passes_test(is_corporativo)
def listar_shoppings(request):
    shoppings = Shopping.objects.all()
    paginator = Paginator(shoppings, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'painel_admin/listar_shoppings.html', {'page_obj': page_obj})

@login_required
@user_passes_test(is_corporativo)
def editar_shopping(request, shopping_id):
    shopping = get_object_or_404(Shopping, id=shopping_id)
    if request.method == 'POST':
        form = ShoppingForm(request.POST, instance=shopping)
        if form.is_valid():
            form.save()
            messages.success(request, "Shopping atualizado com sucesso!")  # <-- aqui ✅
            return redirect('listar_shoppings')
    else:
        form = ShoppingForm(instance=shopping)
    return render(request, 'painel_admin/editar_shopping.html', {'form': form})

@login_required
@user_passes_test(is_corporativo)
def listar_usuarios(request):
    usuarios = Usuario.objects.all().order_by('username')
    paginator = Paginator(usuarios, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'painel_admin/listar_usuarios.html', {'page_obj': page_obj})

@login_required
@user_passes_test(is_corporativo)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")  # <-- aqui ✅
            return redirect('listar_usuarios')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'painel_admin/editar_usuario.html', {'form': form})


@login_required
@user_passes_test(is_corporativo)
def excluir_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuário excluído com sucesso.")
        return redirect('listar_usuarios')
    return render(request, 'painel_admin/confirmar_exclusao_usuario.html', {
        'usuario': usuario,
        'delete_action_url': request.path,
        'cancel_url': reverse('listar_usuarios')
    })


@login_required
@user_passes_test(is_corporativo)
def listar_grupos(request):
    grupos = Group.objects.all()
    paginator = Paginator(grupos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'painel_admin/listar_grupos.html', {'page_obj': page_obj})

@login_required
@user_passes_test(is_corporativo)
def editar_grupo(request, group_id):
    grupo = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        grupo.name = request.POST.get('name')
        grupo.save()
        messages.success(request, "Grupo atualizado com sucesso!")  # ✅ Aqui adiciona a mensagem
        return redirect('listar_grupos')
    return render(request, 'painel_admin/editar_grupo.html', {'grupo': grupo})


@login_required
@user_passes_test(is_corporativo)
def excluir_grupo(request, group_id):
    grupo = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, "Grupo excluído com sucesso.")
        return redirect('listar_grupos')
    return render(request, 'painel_admin/confirmar_exclusao_grupo.html', {
        'grupo': grupo,
        'delete_action_url': request.path,
        'cancel_url': reverse('listar_grupos')
    })

@login_required
@user_passes_test(is_superuser)
def painel_admin_dashboard(request):
    total_shoppings = Shopping.objects.count()
    total_usuarios = Usuario.objects.count()
    total_grupos = Group.objects.count()
    return render(request, 'painel_admin/dashboard.html', {
        'total_shoppings': total_shoppings,
        'total_usuarios': total_usuarios,
        'total_grupos': total_grupos,
    })

@login_required
@user_passes_test(is_superuser)
def criar_shopping(request):
    if request.method == 'POST':
        form = ShoppingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shopping criado com sucesso!")
            return redirect('listar_shoppings')
    else:
        form = ShoppingForm()
    return render(request, 'painel_admin/criar_shopping.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def excluir_shopping(request, shopping_id):
    shopping = get_object_or_404(Shopping, id=shopping_id)
    if request.method == 'POST':
        shopping.delete()
        messages.success(request, "Shopping excluído com sucesso!")
        return redirect('listar_shoppings')
    return render(request, 'painel_admin/confirmar_exclusao_shopping.html', {
        'shopping': shopping,
        'delete_action_url': request.path,
        'cancel_url': reverse('listar_shoppings')
    })

@login_required
@user_passes_test(is_superuser)
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.is_staff = user.is_superuser  # ✅ habilita login no admin se for superuser
            user.shopping = form.cleaned_data.get('shopping')
            user.save()

            # ✅ Forçar salvar grupo
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                user.groups.clear()  # Limpa grupos antigos
                user.groups.add(grupo)  # Adiciona o grupo escolhido

            messages.success(request, "Usuário criado com sucesso!")
            return redirect('listar_usuarios')
    else:
        form = UsuarioCreationForm()

    return render(request, 'usuarios/criar_usuario.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def criar_grupo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            Group.objects.create(name=nome)
            messages.success(request, "Grupo criado com sucesso!")
            return redirect('listar_grupos')
    return render(request, 'painel_admin/criar_grupo.html')


@login_required
@user_passes_test(is_superuser)
def listar_perfis(request):
    perfis = Perfil.objects.select_related('usuario', 'shopping').all()
    paginator = Paginator(perfis, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'painel_admin/listar_perfis.html', {'page_obj': page_obj})

@login_required
@user_passes_test(is_superuser)
def criar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Perfil criado com sucesso!")
            return redirect('listar_perfis')
        else:
            # Verifica se o erro é de duplicidade de usuário
            if 'usuario' in form.errors and any('Perfil com este Usuario já existe.' in erro for erro in form.errors['usuario']):
                messages.error(request, "❌ Já existe um perfil cadastrado para este usuário.")
            else:
                messages.error(request, "❌ Não foi possível criar o perfil. Corrija os erros abaixo.")
    else:
        form = PerfilForm()

    return render(request, 'painel_admin/criar_perfil.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def editar_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Perfil atualizado com sucesso!")
            return redirect('listar_perfis')
        else:
            # Verifica se o erro é de duplicidade de usuário
            if 'usuario' in form.errors and any('Perfil com este Usuario já existe.' in erro for erro in form.errors['usuario']):
                messages.error(request, "❌ Já existe outro perfil cadastrado para este usuário.")
            else:
                messages.error(request, "❌ Não foi possível atualizar o perfil. Corrija os erros abaixo.")
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'painel_admin/editar_perfil.html', {'form': form, 'perfil': perfil})


@login_required
@user_passes_test(is_superuser)
def excluir_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    if request.method == 'POST':
        perfil.delete()
        messages.success(request, "Perfil excluído com sucesso!")
        return redirect('listar_perfis')
    return render(request, 'painel_admin/confirmar_exclusao_perfil.html', {
        'perfil': perfil,
        'delete_action_url': request.path,
        'cancel_url': reverse('listar_perfis')
    })
