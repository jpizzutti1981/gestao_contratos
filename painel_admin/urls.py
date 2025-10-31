from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_admin_dashboard, name='painel_admin_dashboard'),
    
    path('shoppings/', views.listar_shoppings, name='listar_shoppings'),
    path('shoppings/criar/', views.criar_shopping, name='criar_shopping'),
    path('shopping/editar/<int:shopping_id>/', views.editar_shopping, name='editar_shopping'),
    path('shoppings/excluir/<int:shopping_id>/', views.excluir_shopping, name='excluir_shopping'),
    path('shoppings/excluir/<int:shopping_id>/', views.excluir_shopping, name='confirmar_exclusao_shopping'),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuario/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuario/excluir/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),

    path('grupos/', views.listar_grupos, name='listar_grupos'),
    path('grupos/criar/', views.criar_grupo, name='criar_grupo'),
    path('grupo/editar/<int:group_id>/', views.editar_grupo, name='editar_grupo'),
    path('grupo/excluir/<int:group_id>/', views.excluir_grupo, name='excluir_grupo'),

    path('perfis/', views.listar_perfis, name='listar_perfis'),
    path('perfis/criar/', views.criar_perfil, name='criar_perfil'),
    path('perfis/editar/<int:perfil_id>/', views.editar_perfil, name='editar_perfil'),
    path('perfis/excluir/<int:perfil_id>/', views.excluir_perfil, name='excluir_perfil'),
    
]
