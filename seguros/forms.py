from django import forms
from .models import Loja, ApoliceLoja

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = [
            "shopping", "codigo_loja", "nome_fantasia", "razao_social", "cnpj",
            "piso", "unidade", "segmento", "area_m2",
            "contato_nome", "contato_email", "contato_telefone",
            "status_loja", "canal_notificacao_preferencial", "aceite_lgpd", "observacoes",
        ]

class ApoliceLojaForm(forms.ModelForm):
    class Meta:
        model = ApoliceLoja
        fields = [
            "loja", "tipo_seguro", "seguradora", "numero_apolice", "endosso",
            "vigencia_inicio", "vigencia_fim", "data_emissao", "data_recebida",
            "status_compliance", "atende_exigencias", "motivo_nao_conformidade",
            "valor_premio", "franquia_padrao", "condicoes_especiais",
            "arquivo_apolice", "arquivo_certificado", "comprovante_pagamento",
        ]
        widgets = {
            "vigencia_inicio": forms.DateInput(attrs={"type": "date"}),
            "vigencia_fim": forms.DateInput(attrs={"type": "date"}),
            "data_emissao": forms.DateInput(attrs={"type": "date"}),
            "data_recebida": forms.DateInput(attrs={"type": "date"}),
        }