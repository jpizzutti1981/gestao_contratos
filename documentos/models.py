from django.db import models
from django.conf import settings  # ✅ Aqui trocamos para settings.AUTH_USER_MODEL

class Shopping(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10)
    cnpj = models.CharField(max_length=20)
    email_alertas = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome


class RegistroDocumento(models.Model):
    TIPO_CHOICES = (
        ('documento', 'Documento'),
        ('contrato', 'Contrato'),
    )

    shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    data_emissao = models.DateField()
    data_vencimento = models.DateField()
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    status_aprovacao = models.CharField(max_length=20, default='pendente')
    aprovado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='aprovador', blank=True)
    data_aprovacao = models.DateTimeField(blank=True, null=True)
    motivo_reprovacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.tipo})"


# Novo modelo para múltiplos anexos
class AnexoDocumento(models.Model):
    documento = models.ForeignKey(RegistroDocumento, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='uploads/anexos/')
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo de {self.documento.titulo} - {self.arquivo.name}"


class DocumentoObrigatorio(models.Model):
    """Representa um tipo de documento que é obrigatório para um shopping/área/categoria."""
    area = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    nome = models.CharField(max_length=150)
    shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    # Marcação manual feita pelo gestor quando julgar o documento como ok
    marcado_ok = models.BooleanField(default=False)
    marcado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_marcados')
    marcado_em = models.DateTimeField(blank=True, null=True)
    # Vinculação manual de um documento/contrato avulso que atende esta premissa
    documento_vinculado = models.ForeignKey(
        'RegistroDocumento', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='premissas_vinculadas'
    )

    class Meta:
        verbose_name = 'Documento Obrigatório'
        verbose_name_plural = 'Documentos Obrigatórios'

    def __str__(self):
        return f"{self.shopping.nome} - {self.nome}"