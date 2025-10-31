from django.core.management.base import BaseCommand
from django.conf import settings
from documentos.models import RegistroDocumento, AnexoDocumento
import os
import unicodedata


def normalize_filename(name: str) -> str:
    # Normaliza removendo acentos e padronizando underscores
    nfkd_form = unicodedata.normalize('NFKD', name)
    only_ascii = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    return only_ascii.lower().replace(' - ', '_').replace(' ', '_')


class Command(BaseCommand):
    help = "Vincula arquivos legados em /uploads aos documentos como AnexoDocumento"

    def add_arguments(self, parser):
        parser.add_argument('--doc-id', type=int, help='Processar apenas um documento específico')
        parser.add_argument('--dry-run', action='store_true', help='Não cria anexos, apenas mostra o que seria feito')

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        uploads_root = os.path.join(media_root, 'uploads')

        if not os.path.isdir(uploads_root):
            self.stderr.write(self.style.ERROR(f"Diretório de uploads não encontrado: {uploads_root}"))
            return

        docs_qs = RegistroDocumento.objects.all()
        if options.get('doc_id'):
            docs_qs = docs_qs.filter(id=options['doc_id'])

        total_linkados = 0
        for doc in docs_qs:
            # se já houver anexos, pular
            if doc.anexos.exists():
                continue

            base_norm = normalize_filename(doc.titulo or '')
            if not base_norm:
                continue

            candidatos = []

            # procurar em /uploads (legado do campo arquivo)
            try:
                for fname in os.listdir(uploads_root):
                    fpath = os.path.join(uploads_root, fname)
                    if not os.path.isfile(fpath):
                        continue
                    name_no_ext = os.path.splitext(fname)[0]
                    name_norm = normalize_filename(name_no_ext)
                    if name_norm.startswith(base_norm):
                        candidatos.append(('uploads/' + fname, fpath))
            except Exception:
                pass

            # procurar em /uploads/anexos (já na estrutura nova)
            anexos_dir = os.path.join(uploads_root, 'anexos')
            if os.path.isdir(anexos_dir):
                try:
                    for fname in os.listdir(anexos_dir):
                        fpath = os.path.join(anexos_dir, fname)
                        if not os.path.isfile(fpath):
                            continue
                        name_no_ext = os.path.splitext(fname)[0]
                        name_norm = normalize_filename(name_no_ext)
                        if name_norm.startswith(base_norm):
                            candidatos.append(('uploads/anexos/' + fname, fpath))
                except Exception:
                    pass

            # procurar em /uploads/uploads/anexos (arquivos salvos com dup pasta)
            dup_anexos_dir = os.path.join(uploads_root, 'uploads', 'anexos')
            if os.path.isdir(dup_anexos_dir):
                try:
                    for fname in os.listdir(dup_anexos_dir):
                        fpath = os.path.join(dup_anexos_dir, fname)
                        if not os.path.isfile(fpath):
                            continue
                        name_no_ext = os.path.splitext(fname)[0]
                        name_norm = normalize_filename(name_no_ext)
                        if name_norm.startswith(base_norm):
                            candidatos.append(('uploads/uploads/anexos/' + fname, fpath))
                except Exception:
                    pass

            if not candidatos:
                # Logar ausência de candidatos para diagnósticos
                self.stdout.write(f"Doc {doc.id} sem candidatos (titulo='{doc.titulo}', base_norm='{base_norm}')")
                continue

            # evitar criar muitos anexos – limitar a 5 por segurança
            candidatos = candidatos[:5]

            for rel_path, abs_path in candidatos:
                self.stdout.write(f"Doc {doc.id} - vinculando: {rel_path}")
                if options.get('dry_run'):
                    continue
                try:
                    anexo = AnexoDocumento(documento=doc)
                    # apontar diretamente para o caminho relativo dentro de MEDIA_ROOT
                    anexo.arquivo.name = rel_path
                    anexo.save()
                    total_linkados += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Falha ao criar anexo para doc {doc.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Backfill concluído. Anexos criados: {total_linkados}"))