from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from documentos.models import Shopping, DocumentoObrigatorio, RegistroDocumento
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Enviar notificação diária de documentos pendentes para gestores de cada shopping.'

    def handle(self, *args, **options):
        hoje = timezone.now()
        shoppings = Shopping.objects.all()
        total_notificados = 0

        for shopping in shoppings:
            pendentes = []
            obrigatorios = DocumentoObrigatorio.objects.filter(shopping=shopping, ativo=True)
            for doc in obrigatorios:
                existe = RegistroDocumento.objects.filter(shopping=shopping, titulo=doc.nome).exists()
                if not existe:
                    pendentes.append(doc.nome)

            if not pendentes:
                continue

            # Obter e-mails dos gestores do shopping
            destinatarios = []
            try:
                grupo = Group.objects.get(name='Gestor')
                gestores = grupo.user_set.filter(perfil__shopping=shopping)
                destinatarios = [g.email for g in gestores if g.email]
            except Group.DoesNotExist:
                gestores = []

            if not destinatarios:
                # fallback para e-mail de alerta do shopping
                if shopping.email_alertas:
                    destinatarios = [shopping.email_alertas]

            if not destinatarios:
                self.stdout.write(self.style.WARNING(f"Nenhum destinatário configurado para {shopping.nome}, pulando."))
                continue

            assunto = f"Pendências de Documentos – {shopping.nome}"
            corpo = f"Prezado(a) gestor(a),\n\nSeguem os documentos obrigatórios ainda não enviados para {shopping.nome}:\n\n"
            for p in pendentes:
                corpo += f"- {p}\n"
            corpo += "\nEnquanto não inseridos, o sistema continuará notificando diariamente.\n\nAtenciosamente,\nEquipe de Gestão de Contratos"

            try:
                send_mail(assunto, corpo, 'nao-responda@sistema.com', destinatarios, fail_silently=False)
                total_notificados += 1
                self.stdout.write(self.style.SUCCESS(f"Notificações enviadas para {shopping.nome} -> {', '.join(destinatarios)}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao enviar para {shopping.nome}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Tarefa finalizada. Shoppings notificados: {total_notificados}"))
