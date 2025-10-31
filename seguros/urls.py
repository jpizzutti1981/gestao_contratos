from django.urls import path
from .views import ApoliceListView, ApoliceCreateView, LojaCreateView

urlpatterns = [
    path('', ApoliceListView.as_view(), name='seguros_apolice_list'),
    path('apolices/novo/', ApoliceCreateView.as_view(), name='seguros_apolice_novo'),
    path('lojas/novo/', LojaCreateView.as_view(), name='seguros_loja_novo'),
]