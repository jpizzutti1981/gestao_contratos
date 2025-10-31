from django.contrib import admin
from .models import Shopping, RegistroDocumento, AnexoDocumento

@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = ("nome", "sigla", "cnpj", "email_alertas")
    search_fields = ("nome", "sigla", "cnpj")
    list_filter = ("sigla",)

@admin.register(RegistroDocumento)
class RegistroDocumentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "shopping", "status_aprovacao", "data_vencimento")
    list_filter = ("tipo", "status_aprovacao", "shopping")
    search_fields = ("titulo", "descricao")
    readonly_fields = ("data_envio", "enviado_por")

@admin.register(AnexoDocumento)
class AnexoDocumentoAdmin(admin.ModelAdmin):
    list_display = ("documento", "arquivo", "data_upload")
    list_filter = ("data_upload",)
    readonly_fields = ("data_upload",)