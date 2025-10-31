# documentos/models.py

from django.db import models

class Shopping(models.Model):
    nome = models.CharField(max_length=100)
    email_alertas = models.EmailField(blank=True, null=True)  # ⬆️ Adicionado

    def __str__(self):
        return self.nome


