from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from documentos.views import CustomLoginView, CustomLogoutView  # Usa suas views personalizadas

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login e Logout usando suas VIEWS personalizadas ✅
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),

    # Sistema principal
    path('', include('documentos.urls')),

    # Dashboard de Contratos
    path('dashboard/', include('dashboard.urls')),

    # Módulo de Seguros
    path('seguros/', include('seguros.urls')),

    # Painel Administrativo
    path('admin-panel/', include('painel_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
