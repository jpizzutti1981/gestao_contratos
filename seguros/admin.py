from django.contrib import admin
from .models import Loja, ApoliceLoja


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ("shopping", "codigo_loja", "nome_fantasia", "segmento", "status_loja")
    search_fields = ("codigo_loja", "nome_fantasia", "cnpj")
    list_filter = ("shopping", "status_loja", "segmento")


@admin.register(ApoliceLoja)
class ApoliceLojaAdmin(admin.ModelAdmin):
    list_display = (
        "loja",
        "tipo_seguro",
        "seguradora",
        "numero_apolice",
        "vigencia_inicio",
        "vigencia_fim",
        "status_compliance",
        "vencida",
    )
    search_fields = ("numero_apolice", "seguradora", "loja__codigo_loja", "loja__nome_fantasia")
    list_filter = ("tipo_seguro", "status_compliance", "loja__shopping")
