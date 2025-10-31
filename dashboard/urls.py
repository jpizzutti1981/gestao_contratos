from django.urls import path
from .views import DashboardContratosView

urlpatterns = [
    path('', DashboardContratosView.as_view(), name='dashboard_contratos'),
]