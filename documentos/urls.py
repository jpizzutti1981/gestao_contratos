from django.urls import path
from . import views
from .views import CustomLoginView
from documentos.views import CustomLoginView, CustomLogoutView
from .views import ver_historico_documento
from .views import PainelDocumentosView


urlpatterns = [
    # URL raiz - redireciona para o painel
    path('', views.painel_redirect, name='home'),
    # Adicionando a URL para os Perfis
    path('painel/', views.painel_redirect, name='painel_redirect'),
    path('painel/geral/', views.painel_documentos, name='painel_geral'),
    path('painel/gerencial/', PainelDocumentosView.as_view(), name='painel_documentos_gerencial'),
    path('painel/gerencial/status.json', views.painel_documentos_status_json, name='painel_documentos_status_json'),
    path('painel/shopping/<int:shopping_id>/', views.detalhes_shopping, name='detalhes_shopping'),
    path('documento/aprovar/<int:doc_id>/', views.aprovar_documento, name='aprovar_documento'),
    path('documento/novo/', views.novo_documento, name='novo_documento'),
    path('documento/novo/<int:shopping_id>/', views.novo_documento, name='novo_documento_shopping'),
    path('painel/pendencias/', views.pendencias_gestor, name='pendencias_gestor'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('documento/reprovar/<int:doc_id>/', views.reprovar_documento, name='reprovar_documento'),
    path('documento/editar/<str:tipo>/<int:doc_id>/', views.editar_documento, name='editar_documento'),
    path('documento/excluir/<str:tipo>/<int:doc_id>/', views.excluir_documento, name='excluir_documento'),
    path('documento/confirmar-exclusao/<str:tipo>/<int:doc_id>/', views.confirmar_exclusao, name='confirmar_exclusao'),
    path('documento/detalhar/<str:tipo>/<int:doc_id>/', views.detalhar_documento, name='detalhar_documento'),
    path('documento/reaprovar/<int:doc_id>/', views.reenviar_para_aprovacao, name='reenviar_documento'),
    path('documento/historico/<path:titulo>/<int:shopping_id>/', ver_historico_documento, name='ver_historico_documento'),
    path('documento/anexo/excluir/<int:anexo_id>/', views.excluir_anexo, name='excluir_anexo'),

    path('documento/obrigatorio/marcar/<int:doc_obrig_id>/', views.marcar_documento_obrigatorio, name='marcar_documento_obrigatorio'),
    path('documento/obrigatorio/importar/', views.importar_documentos_excel, name='importar_documentos_excel'),
    path('documento/obrigatorio/excluir/<int:doc_obrig_id>/', views.excluir_documento_obrigatorio, name='excluir_documento_obrigatorio'),
    path('documento/obrigatorio/novo/', views.create_documento_obrigatorio, name='create_documento_obrigatorio'),
    path('documento/obrigatorio/vincular/<int:doc_obrig_id>/', views.vincular_documento_obrigatorio, name='vincular_documento_obrigatorio'),
    path('documento/obrigatorio/desvincular/<int:doc_obrig_id>/', views.desvincular_documento_obrigatorio, name='desvincular_documento_obrigatorio'),
    path('documento/obrigatorio/buscar_avulsos/<int:doc_obrig_id>/', views.buscar_documentos_avulsos_json, name='buscar_documentos_avulsos_json'),

    # documentos/urls.py
    path('agenda/', views.agenda_documentos, name='agenda_vencimentos'),
    path('api/vencimentos/', views.api_vencimentos_json, name='api_vencimentos_json'),
    
]
