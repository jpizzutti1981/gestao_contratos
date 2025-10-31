from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from documentos.models import RegistroDocumento
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Verifica documentos com vencimento em 60, 30 e 10 dias e envia alerta por e-mail.'

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()
        dias_alerta = [60, 30, 10]

        for dias in dias_alerta:
            data_alvo = hoje + timedelta(days=dias)

            documentos = RegistroDocumento.objects.filter(
                data_vencimento__range=(data_alvo, data_alvo),
                status_aprovacao='aprovado'
            )

            print(f"🔎 {documentos.count()} documentos vencendo em {dias} dias (alvo: {data_alvo})")

            for doc in documentos:
                shopping = doc.shopping

                grupo_usuario = Group.objects.filter(name="Usuario").first()
                grupo_gestor = Group.objects.filter(name="Gestor").first()

                destinatarios = set()

                if grupo_usuario:
                    usuarios = grupo_usuario.user_set.filter(
                        perfil__shopping=shopping, email__isnull=False
                    ).exclude(email='')
                    destinatarios.update([u.email for u in usuarios])

                if grupo_gestor:
                    gestores = grupo_gestor.user_set.filter(
                        perfil__shopping=shopping, email__isnull=False
                    ).exclude(email='')
                    destinatarios.update([g.email for g in gestores])

                if destinatarios:
                    assunto = f"📅 Alerta: {doc.titulo} vence em {dias} dias"
                    texto = f"O documento {doc.titulo} está prestes a vencer em {dias} dias."

                    html = f"""
                    <h3 style="color:#0d6efd;">📑 Alerta de Vencimento</h3>
                    <p>O documento <strong>{doc.titulo}</strong> está programado para vencer em <strong>{dias} dias</strong>:</p>
                    <ul>
                        <li><strong>Tipo:</strong> {doc.get_tipo_display()}</li>
                        <li><strong>Data de Vencimento:</strong> {doc.data_vencimento.strftime('%d/%m/%Y')}</li>
                        <li><strong>Enviado por:</strong> {doc.enviado_por.get_full_name() or doc.enviado_por.username}</li>
                    </ul>
                    <hr>
                    <p style="font-size:0.9em;color:#888;">Por favor, verifique e tome as providências necessárias.</p>
                    """

                    msg = EmailMultiAlternatives(
                        subject=assunto,
                        body=texto,
                        from_email='nao-responda@sistema.com',
                        to=list(destinatarios)
                    )
                    msg.attach_alternative(html, "text/html")
                    msg.send()

                    print(f"✉️ E-mail enviado para: {', '.join(destinatarios)}")

        self.stdout.write(self.style.SUCCESS("✔️ Verificação de vencimentos concluída e e-mails enviados."))
