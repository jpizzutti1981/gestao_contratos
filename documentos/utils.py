from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import logging
from documentos.models import RegistroDocumento

logger = logging.getLogger(__name__)  # usar logger do Django para registrar erro

def notificar_usuario_documento(doc: RegistroDocumento, tipo='aprovado'):
    assunto = f"📄 Documento {doc.titulo} - {tipo.upper()}"

    if tipo == 'aprovado':
        mensagem = (
            f"Seu documento \"{doc.titulo}\" foi aprovado com sucesso.\n\n"
            f"Status: ✔️ Aprovado\n"
            f"Data: {doc.data_aprovacao.strftime('%d/%m/%Y %H:%M')}\n"
            f"Aprovado por: {doc.aprovado_por.get_full_name() or doc.aprovado_por.username}\n\n"
            "Você pode consultar esse documento acessando o sistema."
        )
    else:
        mensagem = (
            f"Seu documento \"{doc.titulo}\" foi reprovado.\n\n"
            f"Status: ❌ Reprovado\n"
            f"Motivo informado: {doc.motivo_reprovacao}\n"
            f"Data: {doc.data_aprovacao.strftime('%d/%m/%Y %H:%M')}\n"
            f"Responsável: {doc.aprovado_por.get_full_name() or doc.aprovado_por.username}\n\n"
            "Você pode reenviar um novo documento corrigido pelo sistema."
        )

    try:
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[doc.enviado_por.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail de notificação: {e}")
