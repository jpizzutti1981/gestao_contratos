from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = 'Envia e-mails de teste com diferentes tipos de mensagens'

    def handle(self, *args, **kwargs):
        destinatario = "jgcanil@hotmail.com"
        from_email = "gcontratosoper@gmail.com"

        mensagens = [
            {
                "assunto": "📅 Vencimento em 60 dias",
                "html": "<h3>Alerta: Documento vence em 60 dias</h3><p>Confira no sistema.</p>"
            },
            {
                "assunto": "📅 Vencimento em 30 dias",
                "html": "<h3>Alerta: Documento vence em 30 dias</h3><p>Confira no sistema.</p>"
            },
            {
                "assunto": "📅 Vencimento em 10 dias",
                "html": "<h3>Alerta: Documento vence em 10 dias</h3><p>Confira no sistema.</p>"
            },
            {
                "assunto": "✔️ Documento Aprovado",
                "html": "<h3 style='color:green;'>Seu documento foi aprovado</h3><p>Acesse o sistema para visualizar.</p>"
            },
            {
                "assunto": "❌ Documento Reprovado",
                "html": "<h3 style='color:red;'>Seu documento foi reprovado</h3><p>Motivo: Documento ilegível.</p>"
            }
        ]

        for msg in mensagens:
            email = EmailMultiAlternatives(
                subject=msg["assunto"],
                body=msg["assunto"],  # texto plano
                from_email=from_email,
                to=[destinatario]
            )
            email.attach_alternative(msg["html"], "text/html")
            email.send()

        self.stdout.write(self.style.SUCCESS("✅ Todos os e-mails de teste foram enviados."))
