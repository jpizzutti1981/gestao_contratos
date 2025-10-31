from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from documentos.models import RegistroDocumento, AnexoDocumento
import os
import unicodedata
from datetime import timedelta


def normalize(text: str) -> str:
    nfkd = unicodedata.normalize('NFKD', text or '')
    ascii_only = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return ascii_only.lower().replace('-', ' ').replace('_', ' ')


def tokenize(text: str):
    return [t for t in normalize(text).split() if t and t.isalnum()]


def list_candidate_files(media_root):
    candidates = []
    paths = [
        os.path.join(media_root, 'uploads'),
        os.path.join(media_root, 'uploads', 'anexos'),
        os.path.join(media_root, 'uploads', 'uploads', 'anexos'),
    ]
    seen = set()
    for base in paths:
        if not os.path.isdir(base):
            continue
        for fname in os.listdir(base):
            fpath = os.path.join(base, fname)
            if not os.path.isfile(fpath):
                continue
            # construir caminho relativo a MEDIA_ROOT
            rel = os.path.relpath(fpath, media_root).replace('\\', '/').replace('\\', '/')
            if rel in seen:
                continue
            seen.add(rel)
            candidates.append((rel, fpath))
    return candidates


class Command(BaseCommand):
    help = "Vincula anexos órfãos usando similaridade de nome e proximidade de data de envio"

    def add_arguments(self, parser):
        parser.add_argument('--doc-id', type=int, help='Processar apenas um documento específico')
        parser.add_argument('--dry-run', action='store_true', help='Não cria anexos, apenas mostra o que seria feito')
        parser.add_argument('--limit-per-doc', type=int, default=1, help='Número máximo de anexos por documento')
        parser.add_argument('--days-window', type=int, default=3, help='Janela de dias para considerar proximidade temporal')

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT
        if not os.path.isdir(media_root):
            self.stderr.write(self.style.ERROR(f"MEDIA_ROOT inexistente: {media_root}"))
            return

        all_files = list_candidate_files(media_root)
        # ignorar arquivos já vinculados
        linked_names = set(AnexoDocumento.objects.values_list('arquivo', flat=True))
        orphan_files = [(rel, abs) for (rel, abs) in all_files if rel not in linked_names]
        self.stdout.write(f"Arquivos órfãos identificados: {len(orphan_files)}")

        docs_qs = RegistroDocumento.objects.all()
        if options.get('doc_id'):
            docs_qs = docs_qs.filter(id=options['doc_id'])

        total_linkados = 0
        for doc in docs_qs:
            if doc.anexos.exists():
                continue

            doc_tokens = set(tokenize(doc.titulo))
            envio_dt = timezone.make_aware(doc.data_envio) if timezone.is_naive(doc.data_envio) else doc.data_envio
            window = timedelta(days=options['days_window'])

            scored = []
            for rel, abs_path in orphan_files:
                fname = os.path.basename(abs_path)
                f_tokens = set(tokenize(os.path.splitext(fname)[0]))
                overlap = len(doc_tokens & f_tokens)
                try:
                    mtime = timezone.make_aware(timezone.datetime.fromtimestamp(os.path.getmtime(abs_path)))
                    delta = abs((mtime - envio_dt).total_seconds()) if envio_dt else float('inf')
                except Exception:
                    delta = float('inf')

                # score: prioriza nome; usa delta temporal como desempate
                score = overlap * 1000 - (delta / 86400.0)  # dias
                scored.append((score, overlap, delta, rel, abs_path, fname))

            scored.sort(reverse=True)
            chosen = []
            for score, overlap, delta, rel, abs_path, fname in scored:
                # critérios mínimos: pelo menos 1 token comum OU dentro da janela em dias
                if overlap >= 1 or (envio_dt and delta <= window.total_seconds()):
                    chosen.append((rel, abs_path, fname, overlap, delta))
                if len(chosen) >= options['limit_per_doc']:
                    break

            if not chosen:
                self.stdout.write(f"Doc {doc.id} sem match por nome/data (titulo='{doc.titulo}')")
                continue

            for rel, abs_path, fname, overlap, delta in chosen:
                self.stdout.write(f"Doc {doc.id} <- {rel} (overlap={overlap}, delta_dias={delta/86400.0:.2f})")
                if options.get('dry_run'):
                    continue
                try:
                    anexo = AnexoDocumento(documento=doc)
                    anexo.arquivo.name = rel
                    anexo.save()
                    total_linkados += 1
                    # remover do conjunto de órfãos para evitar reuso
                    orphan_files = [(r, a) for (r, a) in orphan_files if r != rel]
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Falha ao vincular {rel} ao doc {doc.id}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Smart backfill concluído. Anexos criados: {total_linkados}"))