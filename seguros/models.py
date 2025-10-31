from django.conf import settings
from django.db import models
from documentos.models import Shopping


class Loja(models.Model):
    STATUS_CHOICES = [
        ("ativa", "Ativa"),
        ("desocupando", "Desocupando"),
        ("encerrada", "Encerrada"),
    ]
    CANAL_CHOICES = [
        ("email", "E-mail"),
        ("whatsapp", "WhatsApp"),
    ]

    shopping = models.ForeignKey(Shopping, on_delete=models.PROTECT, related_name="lojas")
    codigo_loja = models.CharField(max_length=20)
    nome_fantasia = models.CharField(max_length=120)
    razao_social = models.CharField(max_length=160, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)

    piso = models.CharField(max_length=50, blank=True)
    unidade = models.CharField(max_length=50, blank=True)
    segmento = models.CharField(max_length=80, blank=True)
    area_m2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    contato_nome = models.CharField(max_length=120, blank=True)
    contato_email = models.EmailField(blank=True)
    contato_telefone = models.CharField(max_length=30, blank=True)

    status_loja = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ativa")
    canal_notificacao_preferencial = models.CharField(max_length=20, choices=CANAL_CHOICES, default="email")
    aceite_lgpd = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("shopping", "codigo_loja")
        ordering = ["shopping__nome", "codigo_loja"]

    def __str__(self):
        return f"{self.shopping.nome} - {self.codigo_loja} - {self.nome_fantasia}"


class ApoliceLoja(models.Model):
    TIPO_CHOICES = [
        ("rc", "Responsabilidade Civil"),
        ("incendio", "Incêndio"),
        ("multirisco", "Multirisco"),
        ("danos_eletricos", "Danos Elétricos"),
        ("alagamento", "Alagamento"),
        ("outros", "Outros"),
    ]
    COMPLIANCE_CHOICES = [
        ("pendente", "Pendente"),
        ("em_analise", "Em análise"),
        ("aprovada", "Aprovada"),
        ("reprovada", "Reprovada"),
        ("expirada", "Expirada"),
    ]

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="apolices")
    tipo_seguro = models.CharField(max_length=20, choices=TIPO_CHOICES)

    seguradora = models.CharField(max_length=120)
    numero_apolice = models.CharField(max_length=60)
    endosso = models.CharField(max_length=60, blank=True)

    vigencia_inicio = models.DateField()
    vigencia_fim = models.DateField()
    data_emissao = models.DateField(null=True, blank=True)
    data_recebida = models.DateField(null=True, blank=True)

    status_compliance = models.CharField(max_length=20, choices=COMPLIANCE_CHOICES, default="pendente")
    atende_exigencias = models.BooleanField(null=True, blank=True)
    motivo_nao_conformidade = models.TextField(blank=True)

    valor_premio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    franquia_padrao = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    condicoes_especiais = models.TextField(blank=True)

    arquivo_apolice = models.FileField(upload_to="uploads/apolices/", blank=True)
    arquivo_certificado = models.FileField(upload_to="uploads/apolices/", blank=True)
    comprovante_pagamento = models.FileField(upload_to="uploads/apolices/", blank=True)

    responsavel_validacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_validacao = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-vigencia_fim"]

    def __str__(self):
        return f"{self.loja} - {self.seguradora} - {self.numero_apolice}"

    @property
    def vencida(self):
        from datetime import date
        return self.vigencia_fim < date.today()

    def status_prazo(self, janela_dias: int = 60):
        from datetime import date, timedelta
        hoje = date.today()
        if self.vencida:
            return "vencida"
        limite = hoje + timedelta(days=janela_dias)
        if self.vigencia_fim <= limite:
            return "a_vencer"
        return "no_prazo"
